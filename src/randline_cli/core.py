"""Core reservoir-sampling logic — pure functions, no I/O."""
from __future__ import annotations

import random
from typing import Iterable, List, Optional


def reservoir_sample(lines: Iterable[str], n: int, seed: Optional[int] = None) -> List[str]:
    """Select `n` items from `lines` uniformly at random, without replacement.

    Uses single-pass reservoir sampling (Algorithm R): the input is read
    exactly once, item by item, and at most `n` items are ever held in
    memory. This means it works correctly on streams or files far too
    large to fit in memory, unlike approaches that first load everything
    into a list and then call `random.sample`.

    If `lines` yields fewer than `n` items, every item is returned (in
    the order it was read). Raises ValueError if `n` is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    rng = random.Random(seed)
    reservoir: List[str] = []

    for i, line in enumerate(lines):
        if i < n:
            reservoir.append(line)
        else:
            j = rng.randint(0, i)
            if j < n:
                reservoir[j] = line

    return reservoir
