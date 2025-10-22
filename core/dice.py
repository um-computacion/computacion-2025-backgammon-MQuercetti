import random


class Dice:
    """
    A class used to represent dice in the Backgammon game.

    Attributes
    ----------
    __values__ : list of int
        The current values of the dice.

    Methods
    -------
    roll()
        Rolls the dice.
    get_values()
        Returns the current values.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the dice object.
        """
        self.__values__ = [1, 1]  # Default

    def roll(self):
        """
        Rolls the dice.

        Returns
        -------
        list of int
            The new values.
        """
        self.__values__ = [random.randint(1, 6), random.randint(1, 6)]
        return self.__values__

    def get_values(self):
        """
        Returns the current values of the dice.

        Returns
        -------
        list of int
            The values.
        """
        return self.__values__
