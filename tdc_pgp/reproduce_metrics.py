#!/usr/bin/env python3
"""Recompute the submitted Pgp_Broccatelli scores from public predictions."""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "0caa286f8c7478f5e5acb5464481aac226b0e20dec402176bc63eca95cfcb6a9"
EXPECTED_LABELS_SHA256 = "7177388806caeae6e30daaf7cfccf5e618be3b408c9f89021fd1b6efc92a5456"
EXPECTED_VALUES = [
    0.9417488669688083,
    0.9427486003732338,
    0.9450813116502267,
    0.9412823247134097,
    0.9453479072247399,
]


def roc_auc(labels: list[float], scores: list[float]) -> float:
    order = sorted(range(len(scores)), key=scores.__getitem__)
    ranks = [0.0] * len(scores)
    cursor = 0
    while cursor < len(order):
        end = cursor + 1
        while end < len(order) and scores[order[end]] == scores[order[cursor]]:
            end += 1
        rank = (cursor + 1 + end) / 2
        for position in range(cursor, end):
            ranks[order[position]] = rank
        cursor = end
    positives = [i for i, label in enumerate(labels) if label == 1]
    negatives = len(labels) - len(positives)
    return (
        sum(ranks[i] for i in positives) - len(positives) * (len(positives) + 1) / 2
    ) / (len(positives) * negatives)


def main() -> None:
    archive = HERE / "predictions.json.gz"
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise RuntimeError(f"prediction archive hash mismatch: {digest}")
    with gzip.open(archive, "rt") as handle:
        public = json.load(handle)

    labels_path = HERE / "official_test_labels.json"
    labels_digest = hashlib.sha256(labels_path.read_bytes()).hexdigest()
    if labels_digest != EXPECTED_LABELS_SHA256:
        raise RuntimeError(f"label snapshot hash mismatch: {labels_digest}")
    label_snapshot = json.loads(labels_path.read_text())
    expected_ids = [str(row["id"]) for row in label_snapshot["rows"]]
    labels = [float(row["label"]) for row in label_snapshot["rows"]]

    values = []
    for seed, expected in zip([1, 2, 3, 4, 5], EXPECTED_VALUES, strict=True):
        rows = public["rows_by_seed"][str(seed)]
        ids = [str(row["id"]) for row in rows]
        if ids != expected_ids:
            raise RuntimeError(f"row identity/order mismatch for seed {seed}")
        scores = [float(row["prediction"]) for row in rows]
        value = roc_auc(labels, scores)
        if not math.isclose(value, expected, rel_tol=0, abs_tol=1e-15):
            raise RuntimeError(f"metric mismatch for seed {seed}: {value} != {expected}")
        values.append(value)
        print(f"seed {seed}: {value:.12f}")

    print(f"mean: {statistics.mean(values):.12f}")
    print(f"sample standard deviation: {statistics.stdev(values):.12f}")


if __name__ == "__main__":
    main()
