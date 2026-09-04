#!/usr/bin/env python3
"""Verify the two public benchmark artifacts using only the standard library."""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import statistics
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MATERIALS = ROOT / "benchmarks/matbench_v0.1_SciKG_Verify/results.json.gz"
BIOLOGY = ROOT / "tdc_pgp/predictions.json.gz"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_materials() -> None:
    assert digest(MATERIALS) == "3c99171a6a140fda4aaee667445c6d4fa6e3ff20c62836962e50f06d49283d75"
    with gzip.open(MATERIALS, "rt") as handle:
        recording = json.load(handle)
    folds = recording["tasks"]["matbench_dielectric"]["results"]
    assert sorted(folds) == [f"fold_{index}" for index in range(5)]
    assert sum(len(fold["data"]) for fold in folds.values()) == 4_764
    mean_mae = statistics.mean(float(fold["scores"]["mae"]) for fold in folds.values())
    assert math.isclose(mean_mae, 0.24932956785914703, rel_tol=0, abs_tol=1e-15)
    print(f"MatBench dielectric: {mean_mae:.12f} MAE across 4,764 held-out rows")


def verify_biology() -> None:
    assert digest(BIOLOGY) == "0caa286f8c7478f5e5acb5464481aac226b0e20dec402176bc63eca95cfcb6a9"
    completed = subprocess.run(
        [sys.executable, str(ROOT / "tdc_pgp/reproduce_metrics.py")],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    print(completed.stdout.strip())


def verify_additional_biology() -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "tdc_sota/reproduce_metrics.py")],
        cwd=ROOT / "tdc_sota",
        check=True,
        text=True,
        capture_output=True,
    )
    print(completed.stdout.strip())


def verify_additional_materials() -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "matbench_sota/reproduce_metrics.py")],
        cwd=ROOT / "matbench_sota",
        check=True,
        text=True,
        capture_output=True,
    )
    print(completed.stdout.strip())


if __name__ == "__main__":
    verify_materials()
    verify_biology()
    verify_additional_biology()
    verify_additional_materials()
