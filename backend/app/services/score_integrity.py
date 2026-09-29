import hashlib
import json
from typing import Any


def canonicalize_scorecard(scorecard: dict[str, Any]) -> bytes:
    """
    Produce a deterministic representation of a scorecard.
    """

    canonical = json.dumps(
        scorecard,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )

    return canonical.encode("utf-8")


def hash_scorecard(scorecard: dict[str, Any]) -> str:
    """
    Return the SHA-256 hash of a scorecard.
    """

    payload = canonicalize_scorecard(scorecard)

    return hashlib.sha256(payload).hexdigest()