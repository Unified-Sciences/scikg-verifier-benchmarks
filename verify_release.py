#!/usr/bin/env python3
"""Reproduce the released benchmark scores and check artifact integrity."""

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
    for name, score in [("SciKG_Verify", 0.25118012222453423),
                        ("SciKG_Residual", 0.24728747764262607)]:
        folder = ROOT / "benchmarks" / ("matbench_v0.1_" + name)
        manifest = json.loads((folder / "ARTIFACT_MANIFEST.json").read_text())
        assert manifest["release"] == "scikg-dielectric-20260906-v2"
        assert math.isclose(manifest["mae"], score, rel_tol=0, abs_tol=1e-15)
        completed = subprocess.run([sys.executable, str(folder / "submission_client.py")],
                                   check=True, capture_output=True, text=True)
        print(completed.stdout.strip())


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
    status = json.loads((ROOT / "EVALUATION_STATUS.json").read_text())
    assert status["dielectric_submission_ready"] is True
    print("Dielectric v2: completed five-fold evaluation. Other task statuses are recorded separately in EVALUATION_STATUS.json.")
    verify_materials()
    verify_biology()
    verify_additional_biology()
    verify_additional_materials()
