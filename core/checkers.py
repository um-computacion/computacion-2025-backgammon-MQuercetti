from core.player import Player

class Checkers:
    """
    A class used to represent a checker piece in the game.

    Attributes
    ----------
    owner : Player
        The player who owns this checker.

    Methods
    -------
    __repr__()
        Returns a string representation of the checker.
    """

    def __init__(self, owner: Player):
        """
        Parameters
        ----------
        owner : Player
            The player who owns this checker.
        """
        self.owner = owner

    def __repr__(self):
        """
        Returns a string representation of the checker.

        Returns
        -------
        str
            A string in the format 'Checkers(owner)'.

        Examples
        --------
        >>> from core.player import Player
        >>> p = Player("Alice", "white")
        >>> c = Checkers(p)
        >>> repr(c)
        'Checkers(player(Alice))'
        """
        return f"Checkers({self.owner})"
