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
    __str__()
        Returns a string representation of the player.
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

    def __str__(self):
        """
        Returns a string representation of the player.

        Returns
        -------
        str
            A string with the player's name and color.
        """
        return f"{self.__name__} ({self.__color__})"
