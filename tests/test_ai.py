from typing import TYPE_CHECKING, List, Any
import copy
import random

if TYPE_CHECKING:
    from core.board import Board
    from core.player import Player


class AIPlayer:
    """
    A class used to represent an AI player in the Backgammon game.

    Attributes
    ----------
    __board__ : Board
        The game board.
    __player__ : Player
        The player this AI controls.

    Methods
    -------
    _get_valid_moves(dice)
        Returns a list of valid moves for the AI.
    _evaluate_board()
        Evaluates the current board state.
    play_turn(dice)
        Makes a move based on the dice.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the AI player object.
        """
        self.__board__ = None
        self.__player__ = None

    def _get_valid_moves(self, dice: List[int]):
        """
        Gets all valid moves for the AI player given the dice.

        Parameters
        ----------
        dice : list of int
            The dice values.

        Returns
        -------
        list
            A list of valid moves.
        """
        valid_moves = []
        # Primero, chequear bar si hay fichas
        if len(self.__board__.get_bar()[self.__player__]) > 0:
            bar_point = -1 if self.__player__.get_color() == "white" else 24  # Usa getter
            for die in dice:
                if self.__board__.is_valid_move(bar_point, die, self.__player__):
                    valid_moves.append((bar_point, die))
        # Luego, movimientos normales
        for die in dice:
            for point in range(24):
                if self.__board__.is_valid_move(point, die, self.__player__):
                    valid_moves.append((point, die))
        return valid_moves

    def _evaluate_board(self):
        """
        Evaluates the current board state for the AI.

        Returns
        -------
        int
            A score for the board state.
        """
        score = 0
        for point in range(24):
            checkers = self.__board__.get_point(point)
            if checkers and checkers[0].get_owner() == self.__player__:  # Usa getter
                score += len(checkers)
        return score

    def play_turn(self, dice: List[int]):
        """
        Plays a turn for the AI player.

        Parameters
        ----------
        dice : list of int
            The dice values.

        Returns
        -------
        None
        """
        valid_moves = self._get_valid_moves(dice)
        if valid_moves:
            move = valid_moves[0]  # Simple: take first valid move
            self.__board__.move_piece(move[0], move[1], self.__player__)

    def _choose_best_sequence(self, board, sequences, player):
        """
        Chooses the best sequence based on evaluation.

        Parameters
        ----------
        board : Board
            The board.
        sequences : list of lists
            List of sequences.
        player : Player
            The player.

        Returns
        -------
        list
            The best sequence.
        """
        best_seq = None
        best_score = -float('inf')
        for seq in sequences:
            score = self._evaluate_sequence(board, seq, player)
            if score > best_score:
                best_score = score
                best_seq = seq
        return best_seq

    def _copy_board(self, board):
        """
        Creates a copy of the board.

        Parameters
        ----------
        board : Board
            The board to copy.

        Returns
        -------
        Board
            A copy of the board.
        """
        import copy
        return copy.deepcopy(board)

    def _evaluate_sequence(self, board, seq, player):
        """
        Evaluates a sequence of moves.

        Parameters
        ----------
        board : Board
            The board.
        seq : list
            The sequence.
        player : Player
            The player.

        Returns
        -------
        int
            A score (example: number of checkers in home).
        """
        copy_board = self._copy_board(board)
        for move in seq:
            copy_board.move_piece(move[0], move[1], player)  # Aplica la secuencia
        score = 0
        color = player.get_color()  # Usa getter
        home_range = range(18, 24) if color == "white" else range(0, 6)
        for point in home_range:
            checkers = copy_board.get_point(point)
            if checkers and checkers[0].get_owner() == player:  # Usa getter
                score += len(checkers)
        return score