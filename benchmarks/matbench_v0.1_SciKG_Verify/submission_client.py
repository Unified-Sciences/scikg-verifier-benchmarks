"""Client for reproducing the submitted MatBench predictions."""

from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen


def verify_materials(endpoint: str, fold: int, candidates: list[dict]) -> list[dict]:
    base_url = os.environ.get(
        "SCIENTIA_VERIFIER_API_URL", "https://unified-sciences.com"
    ).rstrip("/")
    api_key = os.environ.get("SCIENTIA_VERIFIER_API_KEY")
    payload = json.dumps({
        "endpoint": endpoint,
        "fold": fold,
        "candidates": candidates,
    }).encode("utf-8")
    request = Request(
        f"{base_url}/v1/verify/materials",
        data=payload,
        headers={
            **({"Authorization": f"Bearer {api_key}"} if api_key else {}),
            "Content-Type": "application/json",
            "User-Agent": "SciKG-Verify-Reproduction/1.0",
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
