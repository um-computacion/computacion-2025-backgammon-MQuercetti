from typing import Any

class Player:
    """
    A class used to represent a player in the game.

    Attributes
    ----------
    name : str
        The name of the player.
    color : str
        The color of the player's pieces ('white' or 'black').

    Methods
    -------
    __repr__()
        Returns a string representation of the player.
    __eq__(other)
        Compares two players based on their names.
    """

    def __init__(self, name: str, color: str):
        """
        Parameters
        ----------
        name : str
            The name of the player.
        color : str
            The color of the player's pieces ('white' or 'black').
        """
        self.name = name
        self.color = color

    def __repr__(self):
        """
        Returns a string representation of the player.

        Returns
        -------
        str
            A string in the format 'player(name)'.

        Examples
        --------
        >>> p = Player("Alice", "white")
        >>> repr(p)
        'player(Alice)'
        """
        return f"player({self.name})"

    def __eq__(self, other: Any) -> bool:
        """
        Compares two players based on their names.

        Parameters
        ----------
        other : Player
            The player to compare with.

        Returns
        -------
        bool
            True if both players have the same name, False otherwise.

        Examples
        --------
        >>> p1 = Player("Alice", "white")
        >>> p2 = Player("Alice", "white")
        >>> p1 == p2
        True
        """
        if isinstance(other, Player):
            return self.name == other.name
        return False
