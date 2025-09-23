import random
from typing import List

def roll_dice() -> List[int]:
    """
    A function used to represent a dice roll.

    When called, two random values between 1 and 6 are generated.
    If both dice are equal, four values of that number are returned (standard rule in
    games like backgammon).

    Returns
    -------
    list[int]
        A list with the dice values: [d1, d2] or [d, d, d, d] for doubles.

    Examples
    --------
    >>> roll_dice()
    [3, 5]
    >>> # For doubles (random, but example):
    >>> # roll_dice() could return [4, 4, 4, 4]
    """
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    if d1 == d2:
        return [d1] * 4  # Four moves of the same value
    return [d1, d2]

