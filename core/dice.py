class dice:
    """
    A class used to represent a dice roll.

    When initialized, two random values between 1 and 6 are generated.
    If both dice are equal, their values are doubled (common rule in
    games like backgammon).

    Attributes
    ----------
    dice1 : int
        The value of the first die.
    dice2 : int
        The value of the second die.

    Methods
    -------
    roll()
        Generates two random dice values and applies the doubling rule.
    """

    def __init__(self):
        """
        Initializes two dice with random values between 1 and 6.

        If both dice have the same value, their values are doubled.
        """
        import random
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        if self.dice1 == self.dice2:
            self.dice1 *= 2
            self.dice2 *= 2
