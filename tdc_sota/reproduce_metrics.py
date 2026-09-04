#!/usr/bin/env python3
"""Recompute public TDC headline metrics using only the exported predictions."""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import statistics
from pathlib import Path


HERE = Path(__file__).resolve().parent


def ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    result = [0.0] * len(values)
    cursor = 0
    while cursor < len(order):
        end = cursor + 1
        while end < len(order) and values[order[end]] == values[order[cursor]]:
            end += 1
        rank = (cursor + 1 + end) / 2
        for position in range(cursor, end):
            result[order[position]] = rank
        cursor = end
    return result


def roc_auc(labels: list[float], scores: list[float]) -> float:
    score_ranks = ranks(scores)
    positives = [index for index, label in enumerate(labels) if label == 1]
    negatives = len(labels) - len(positives)
    return (
        sum(score_ranks[index] for index in positives)
        - len(positives) * (len(positives) + 1) / 2
    ) / (len(positives) * negatives)


def pearson(left: list[float], right: list[float]) -> float:
    left_mean, right_mean = statistics.mean(left), statistics.mean(right)
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right, strict=True))
    denominator = math.sqrt(
        sum((a - left_mean) ** 2 for a in left)
        * sum((b - right_mean) ** 2 for b in right)
    )
    return numerator / denominator


def metric(name: str, labels: list[float], predictions: list[float]) -> float:
    if name == "roc-auc":
        return roc_auc(labels, predictions)
    if name == "spearman":
        return pearson(ranks(labels), ranks(predictions))
    if name == "mae":
        return statistics.mean(abs(label - prediction) for label, prediction in zip(labels, predictions, strict=True))
    raise ValueError(f"unsupported metric: {name}")


def main() -> None:
    receipt = json.loads((HERE / "REPRODUCTION_RECEIPT.json").read_text())
    archive = HERE / "predictions.json.gz"
    observed_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
    if observed_hash != receipt["predictions_sha256"]:
        raise RuntimeError("prediction archive hash mismatch")
    with gzip.open(archive, "rt") as handle:
        bundle = json.load(handle)

    for endpoint, expected in receipt["endpoints"].items():
        record = bundle["endpoints"][endpoint]
        values = []
        for seed in record["seeds"]:
            rows = seed["rows"]
            labels = [float(row["label"]) for row in rows]
            predictions = [float(row["prediction"]) for row in rows]
            value = metric(record["metric"], labels, predictions)
            expected_value = expected["seed_values"][seed["seed"] - 1]
            if not math.isclose(value, expected_value, rel_tol=0, abs_tol=1e-12):
                raise RuntimeError(
                    f"{endpoint} seed {seed['seed']} mismatch: {value} != {expected_value}"
                )
            values.append(value)
        mean = statistics.mean(values)
        if not math.isclose(mean, expected["mean"], rel_tol=0, abs_tol=1e-12):
            raise RuntimeError(f"{endpoint} mean mismatch: {mean} != {expected['mean']}")
        print(f"{endpoint}: {mean:.12f} {record['metric']} across {len(values)} seeds")


if __name__ == "__main__":
    main()
