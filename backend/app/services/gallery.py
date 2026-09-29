import random
from typing import Sequence


def randomized_projects(
    projects: Sequence,
    seed: int | None = None,
) -> list:
    """
    Randomize project display order.

    A supplied seed produces a deterministic order, allowing a user
    to see the same ordering across pagination/session requests.
    """

    result = list(projects)

    rng = random.Random(seed)
    rng.shuffle(result)

    return result