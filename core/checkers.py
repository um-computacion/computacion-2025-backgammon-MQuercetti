from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.player import Player


class Checkers:
    """
    A class used to represent a checker in the Backgammon game.

    Attributes
    ----------
    __owner__ : Player
        The player who owns the checker.

    Methods
    -------
    get_owner()
        Getter for owner.
    """

    def __init__(self, owner: 'Player'):
        """
        Constructs all the necessary attributes for the checker object.

        Parameters
        ----------
        owner : Player
            The player who owns the checker.
        """
        self.__owner__ = owner

    def get_owner(self):
        """Getter for owner."""
        return self.__owner__