class Player:
    """
    A class used to represent a player in the Backgammon game.

    Attributes
    ----------
    __name__ : str
        The name of the player.
    __color__ : str
        The color of the player ('white' or 'black').

    Methods
    -------
    __eq__(other)
        Checks equality based on name.
    __repr__()
        Returns a string representation of the player.
    __hash__()
        Returns a hash value for the player.
    get_name()
        Getter for name.
    get_color()
        Getter for color.
    """

    def __init__(self, name: str, color: str):
        """
        Constructs all the necessary attributes for the player object.

        Parameters
        ----------
        name : str
            The name of the player.
        color : str
            The color of the player ('white' or 'black').
        """
        self.__name__ = name
        self.__color__ = color

    def __eq__(self, other):
        """
        Checks if two players are equal based on name (color ignored for equality).

        Parameters
        ----------
        other : Player
            The other player to compare.

        Returns
        -------
        bool
            True if equal, False otherwise.
        """
        if not isinstance(other, Player):
            return False
        return self.__name__ == other.__name__  # Solo por nombre

    def __repr__(self):
        """
        Returns a string representation of the player.

        Returns
        -------
        str
            String representation.
        """
        return f"Player(name='{self.__name__}', color='{self.__color__}')"

    def __hash__(self):
        """
        Returns a hash value for the player based on name.

        Returns
        -------
        int
            Hash value.
        """
        return hash(self.__name__)  # Solo por nombre

    def get_name(self):
        """Getter for name."""
        return self.__name__

    def get_color(self):
        """Getter for color."""
        return self.__color__