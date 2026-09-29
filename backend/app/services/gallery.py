import random
from typing import Sequence


def randomized_projects(
    projects: Sequence,
    seed: int | None = None,
) -> list:
    """
    Return projects in a deterministic randomized order.

    The same seed produces the same ordering, which allows a gallery
    session to keep a stable randomized ballot.
    """
    result = list(projects)
    random.Random(seed).shuffle(result)
    return result