from core.player import Player
from core.dice import dice
from core.checkers import Checkers as checkers


class Board:
    """
    A class used to represent a Backgammon game board.

    ...

    Attributes
    ----------
    player1 : player
        The first player of the game.
    player2 : player
        The second player of the game.
    dice1 : dice
        First dice used for rolling.
    dice2 : dice
        Second dice used for rolling.
    winner : player or None
        The player who has won the game, or None if the game is ongoing.
    current_player : player
        The player whose turn it is.
    points : list of list of checkers
        A list of 24 points representing positions on the board, each containing a stack of checkers.

    Methods
    -------
    get_point(index)
        Returns the list of checkers at a specific board point.
    can_move(from_point, to_point, player)
        Checks if a move is valid for the given player from one point to another.
    move_checker(from_point, to_point, player)
        Moves a checker from one point to another if the move is valid.
    """

    def __init__(self, player1: Player, player2: Player):
        """
        Constructs all the necessary attributes for the board object.

        Parameters
        ----------
        player1 : player
            The first player.
        player2 : player
            The second player.
        """
        self.player1 = player1
        self.player2 = player2
        self.dice1 = dice()
        self.dice2 = dice()
        self.winner = None
        self.current_player = player1
        self.points = self._create_points()

    def _create_points(self):
        """
        Initializes the board points with the standard backgammon starting position.

        Returns
        -------
        list
            A list of 24 elements, each a list of checkers representing a board point.
        """
        points = [None] * 24
        points[0] = [checkers(self.player2)] * 2
        points[11] = [checkers(self.player2)] * 5
        points[16] = [checkers(self.player2)] * 3
        points[18] = [checkers(self.player2)] * 5

        points[23] = [checkers(self.player1)] * 2
        points[12] = [checkers(self.player1)] * 5
        points[7] = [checkers(self.player1)] * 3
        points[5] = [checkers(self.player1)] * 5

        for i in range(24):
            if points[i] is None:
                points[i] = []
        return points

    def get_point(self, index: int):
        """
        Returns the checkers at a given board point.

        Parameters
        ----------
        index : int
            Index of the point (0 to 23)

        Returns
        -------
        list
            The list of checkers at the specified point.

        Raises
        ------
        IndexError
            If the index is outside the valid range (0–23).
        """
        if 0 <= index < 24:
            return self.points[index]
        raise IndexError("Invalid point index")

    def can_move(self, from_point: int, to_point: int, player):
        """
        Determines if a move is valid for the given player.

        Parameters
        ----------
        from_point : int
            The index of the point to move from.
        to_point : int
            The index of the point to move to.
        player : player
            The player attempting the move.

        Returns
        -------
        bool
            True if the move is valid, False otherwise.
        """
        if not self.points[from_point]:
            return False
        checker = self.points[from_point][-1]
        if checker.owner != player:
            return False
        destination = self.points[to_point]
        if destination and destination[0].owner != player and len(destination) > 1:
            return False
        return True

    def move_checker(self, from_point: int, to_point: int, player):
        """
        Moves a checker from one point to another on the board.

        If the destination contains a single opposing checker, it is captured.

        Parameters
        ----------
        from_point : int
            The index of the point to move from.
        to_point : int
            The index of the point to move to.
        player : player
            The player making the move.

        Raises
        ------
        ValueError
            If the move is not valid.
        """
        if not self.can_move(from_point, to_point, player):
            raise ValueError("Movimiento inválido")
        checker = self.points[from_point].pop()
        destination = self.points[to_point]
        if destination and destination[0].owner != player and len(destination) == 1:
            captured = destination.pop()
            # Aquí podrías enviar la ficha capturada a la barra
        self.points[to_point].append(checker)

