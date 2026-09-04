#!/usr/bin/env python3
"""Recompute four public MatBench headline scores from held-out predictions."""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import statistics
from pathlib import Path


HERE = Path(__file__).resolve().parent


def score(metric: str, rows: list[dict]) -> float:
    if metric == "mae":
        return statistics.mean(abs(float(row["target"]) - float(row["prediction"])) for row in rows)
    if metric == "balanced_accuracy":
        labels = [int(row["target"]) for row in rows]
        predicted = [int(float(row["prediction"]) >= 0.5) for row in rows]
        true_positive = sum(label == 1 and guess == 1 for label, guess in zip(labels, predicted, strict=True))
        false_negative = sum(label == 1 and guess == 0 for label, guess in zip(labels, predicted, strict=True))
        true_negative = sum(label == 0 and guess == 0 for label, guess in zip(labels, predicted, strict=True))
        false_positive = sum(label == 0 and guess == 1 for label, guess in zip(labels, predicted, strict=True))
        return 0.5 * (
            true_positive / (true_positive + false_negative)
            + true_negative / (true_negative + false_positive)
        )
    raise ValueError(f"unsupported metric: {metric}")


def main() -> None:
    receipt = json.loads((HERE / "REPRODUCTION_RECEIPT.json").read_text())
    archive = HERE / "predictions.json.gz"
    observed = hashlib.sha256(archive.read_bytes()).hexdigest()
    if observed != receipt["predictions_sha256"]:
        raise RuntimeError("prediction archive hash mismatch")
    with gzip.open(archive, "rt") as handle:
        bundle = json.load(handle)
    for endpoint, expected in receipt["endpoints"].items():
        record = bundle["endpoints"][endpoint]
        values = []
        for fold in record["folds"]:
            value = score(record["metric"], fold["rows"])
            expected_value = expected["fold_values"][int(fold["fold"])]
            if not math.isclose(value, expected_value, rel_tol=0, abs_tol=1e-12):
                raise RuntimeError(f"{endpoint} fold {fold['fold']} mismatch: {value} != {expected_value}")
            values.append(value)
        mean = statistics.mean(values)
        if not math.isclose(mean, expected["mean"], rel_tol=0, abs_tol=1e-12):
            raise RuntimeError(f"{endpoint} mean mismatch: {mean} != {expected['mean']}")
        print(f"{endpoint}: {mean:.12f} {record['metric']} across {len(values)} folds")


if __name__ == "__main__":
    main()
