from collections import defaultdict
from time import monotonic
from typing import Dict


RATE_LIMIT = 10
RATE_WINDOW_SECONDS = 60

_vote_requests: Dict[str, list[float]] = defaultdict(list)


def check_rate_limit(identity: str) -> None:
    """
    Simple process-local rate limiter.

    Maximum 10 vote attempts per identity in 60 seconds.
    """

    now = monotonic()

    timestamps = _vote_requests[identity]

    timestamps[:] = [
        timestamp
        for timestamp in timestamps
        if now - timestamp < RATE_WINDOW_SECONDS
    ]

    if len(timestamps) >= RATE_LIMIT:
        raise ValueError(
            "Too many vote requests. Please try again later."
        )

    timestamps.append(now)


def calculate_vote_anomaly(
    recent_vote_count: int,
    same_ip_count: int,
    same_fingerprint_count: int,
) -> bool:
    """
    Returns True when voting behaviour is suspicious.

    Thresholds are intentionally conservative for hackathon use.
    """

    if recent_vote_count >= 50:
        return True

    if same_ip_count >= 25:
        return True

    if same_fingerprint_count >= 10:
        return True

    return False