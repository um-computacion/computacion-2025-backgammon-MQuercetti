from core.player import Player


class Checkers:
    """
    A class used to represent a checker (ficha) in the Backgammon game.

    Attributes
    ----------
    __owner__ : Player
        The player who owns this checker.

    Methods
    -------
    __str__()
        Returns a string representation of the checker.
    """

    def __init__(self, owner: Player):
        """
        Constructs all the necessary attributes for the checker object.

        Parameters
        ----------
        owner : Player
            The player who owns this checker.
        """
        self.__owner__ = owner

    def __str__(self):
        """
        Returns a string representation of the checker.

        Returns
        -------
        str
            A string with the owner's name and color.
        """
        return f"Checker owned by {self.__owner__}"
