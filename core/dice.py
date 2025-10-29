import random

class Dice:
    """
    A class used to represent dice in the Backgammon game.

    Attributes
    ----------
    values : list of int
        The current values of the dice.
    """

    def __init__(self):
        """Constructs all the necessary attributes for the dice object."""
        self.values = []

    def roll(self):
        """Rolls two dice."""
        self.values = [random.randint(1, 6), random.randint(1, 6)]
        return self.values

    def roll_one(self):
        """Rolls a single die."""
        return random.randint(1, 6)

    def get_values(self):
        """Returns the current values of the dice."""
        return self.values

    def set_values(self, values):
        """Sets the dice to specific values."""
        self.values = values

    def remove_value(self, value):
        """Removes a die value after it has been used for a move."""
        if value in self.values:
            self.values.remove(value)
        else:
            raise ValueError(f"Die value {value} not available in {self.values}")
