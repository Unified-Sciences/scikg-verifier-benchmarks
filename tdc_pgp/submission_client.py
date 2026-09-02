"""Client for reproducing the submitted TDC P-gp predictions."""

from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen


def verify_pgp(seed: int, candidates: list[dict]) -> list[dict]:
    """Return predictions for one official TDC seed without changing row order."""
    if seed not in {1, 2, 3, 4, 5}:
        raise ValueError("seed must be one of the official seeds 1, 2, 3, 4, 5")
    base_url = os.environ["SCIENTIA_VERIFIER_API_URL"].rstrip("/")
    api_key = os.environ["SCIENTIA_VERIFIER_API_KEY"]
    payload = json.dumps(
        {
            "benchmark": "Pgp_Broccatelli",
            "seed": seed,
            "candidates": candidates,
        }
    ).encode("utf-8")
    request = Request(
        f"{base_url}/v1/verify/biology",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=300) as response:
        body = json.load(response)
    predictions = body.get("predictions")
    if not isinstance(predictions, list) or len(predictions) != len(candidates):
        raise RuntimeError("verifier API returned a malformed prediction batch")
    expected = [str(row["id"]) for row in candidates]
    received = [str(row["id"]) for row in predictions]
    if received != expected:
        raise RuntimeError("verifier API changed candidate order or identity")
    return predictions
