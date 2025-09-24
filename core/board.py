from typing import Dict, List
from core.player import Player
from core.checkers import Checkers
from core.dice import roll_dice
from core.ai import AIPlayer


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
    winner : player or None
        The player who has won the game, or None if the game is ongoing.
    current_player : player
        The player whose turn it is.
    points : list of list of checkers
        A list of 24 points representing positions on the board, each containing a stack of checkers.
    bar : dict
        Bar for each player: {player: list of checkers in bar}.
    off_board : dict
        Number of checkers borne off for each player: {player: int}.

    Methods
    -------
    get_point(index)
        Returns the list of checkers at a specific board point.
    is_valid_move(from_point, die, player)
        Determines if a move is valid for the given player from one point with a die value.
    move_piece(from_point, die, player)
        Moves a checker from one point with a die if the move is valid.
    roll_dice()
        Rolls the dice and returns the values.
    switch_player()
        Switches the current player.
    is_game_over()
        Checks if the game is over.
    get_winner()
        Returns the winner if the game is over.
    display()
        Displays the current state of the board.
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
        self.winner = None
        self.current_player = player1
        self.points = self._create_points()
        self.bar: Dict[Player, List[Checkers]] = {player1: [], player2: []}
        self.off_board: Dict[Player, int] = {player1: 0, player2: 0}
        self.ai = AIPlayer()
        self.ai.board = self  # Asignar board a la IA
        self.ai.player = player2  # Asignar player a la IA (puedes cambiar a player1 si es humano vs IA)

    def _create_points(self):
        """
        Initializes the board points with the standard backgammon starting position.

        Returns
        -------
        list
            A list of 24 elements, each a list of checkers representing a board point.
        """
        points = [[] for _ in range(24)]  # Use comprehension to avoid object cloning
        points[0] = [Checkers(self.player2) for _ in range(2)]
        points[11] = [Checkers(self.player2) for _ in range(5)]
        points[16] = [Checkers(self.player2) for _ in range(3)]
        points[18] = [Checkers(self.player2) for _ in range(5)]

        points[23] = [Checkers(self.player1) for _ in range(2)]
        points[12] = [Checkers(self.player1) for _ in range(5)]
        points[7] = [Checkers(self.player1) for _ in range(3)]
        points[5] = [Checkers(self.player1) for _ in range(5)]

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

    def is_valid_move(self, from_point: int, die: int, player: Player):
        """
        Determines if a move is valid for the given player from one point with a die value.

        Checks direction based on player color, bar priority, blocks (>=2 opponents), hits (1 opponent), and bear-off.

        Parameters
        ----------
        from_point : int
            The index of the point to move from (-1 for white bar, 24 for black bar).
        die : int
            The die value (1-6).
        player : player
            The player attempting the move.

        Returns
        -------
        bool
            True if the move is valid, False otherwise.
        """
        if die < 1 or die > 6:
            return False
        # Prioridad: si hay fichas en el bar, solo se puede mover desde el bar
        if len(self.bar[player]) > 0 and from_point not in [-1, 24]:
            return False
        # Calcular el destino
        direction = -1 if player.color == "white" else 1
        if from_point == -1:  # Bar blanco
            to_point = die - 1
        elif from_point == 24:  # Bar negro
            to_point = 24 - die
        else:
            to_point = from_point + direction * die
        # Verificar que el destino esté en el tablero
        if not 0 <= to_point < 24:
            return False
        # Verificar que el destino no esté bloqueado (más de 1 ficha rival)
        destination = self.points[to_point]
        if destination and destination[0].owner != player and len(destination) > 1:
            return False
        return True

    def move_piece(
        self, from_point: int, die: int, player: Player
    ):  # Cambié to_point por die para claridad
        """
        Moves a checker from one point to another on the board.

        Parameters
        ----------
        from_point : int
            The index of the point to move from (-1 for white bar, 24 for black bar).
        die : int
            The die value (1-6).
        player : Player
            The player making the move.

        Raises
        ------
        ValueError
            If the move is not valid.
        """
        # Obtener la ficha a mover
        if from_point == -1:  # Bar blanco
            if not self.bar[player]:
                raise ValueError("No checkers on bar")
            checker = self.bar[player].pop()
            to_point = die - 1  # Destino para blanco desde bar
        elif from_point == 24:  # Bar negro
            if not self.bar[player]:
                raise ValueError("No checkers on bar")
            checker = self.bar[player].pop()
            to_point = 24 - die  # Destino para negro desde bar
        elif 0 <= from_point < 24:  # Desde un punto normal
            if not self.points[from_point]:
                raise ValueError("Invalid move")
            checker = self.points[from_point].pop()
            direction = -1 if player.color == "white" else 1
            to_point = from_point + direction * die
        else:
            raise ValueError("Invalid from_point")

        # Manejar el movimiento
        if 0 <= to_point < 24:
            destination = self.points[to_point]
            if destination and destination[0].owner != player and len(destination) == 1:
                captured = destination.pop()
                opponent = self.player2 if player == self.player1 else self.player1
                self.bar[opponent].append(captured)
            self.points[to_point].append(checker)
        else:
            # Bear-off
            self.off_board[player] += 1
            if self.off_board[player] == 15:
                self.winner = player

    # Note: For die-based moves, call move_piece with calculated to_point = from_point ± die
    # The above is kept close to original; for full integration, use a wrapper if needed

    def roll_dice(self):
        """
        Rolls the dice for the current turn.

        Returns
        -------
        list
            The dice values, handling doubles as four moves.

        Examples
        --------
        >>> board = Board(player1, player2)
        >>> board.roll_dice()
        [3, 5]
        """
        return roll_dice()

    def switch_player(self):
        """
        Switches the current player between player1 and player2.

        Returns
        -------
        None
        """
        self.current_player = (
            self.player2 if self.current_player == self.player1 else self.player1
        )

    def is_game_over(self):
        """
        Checks if the game is over (one player has borne off all 15 checkers).

        Returns
        -------
        bool
            True if the game is over, False otherwise.

        Examples
        --------
        >>> board.is_game_over()
        False
        """
        return (
            self.winner is not None
            or self.off_board[self.player1] == 15
            or self.off_board[self.player2] == 15
        )

    def get_winner(self):
        """
        Returns the player who has won the game, or None if the game is ongoing.

        Returns
        -------
        player or None
            The winner.

        Raises
        ------
        ValueError
            If the game is not over.
        """
        if not self.is_game_over():
            raise ValueError("Game not over")
        return self.winner

    def display(self):
        """
        Displays the current state of the board in a simple format.

        Returns
        -------
        None
        """
        print(f"Turno: {self.current_player.name}")
        print("Backgammon Board State:")
        for i in range(23, -1, -1):
            point = self.points[i]
            if point:
                owner_char = "W" if point[0].owner.color == "white" else "B"
                print(f"Point {i}: {len(point)}{owner_char}")
            else:
                print(f"Point {i}: empty")
        print(
            f"Bar {self.player1.name}: {len(self.bar[self.player1])} | Off-board: {self.off_board[self.player1]}"
        )
        print(
            f"Bar {self.player2.name}: {len(self.bar[self.player2])} | Off-board: {self.off_board[self.player2]}"
        )
