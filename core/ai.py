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
    make_move(dice)
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
            if checkers and checkers[0].owner == self.__player__:
                score += len(checkers)
        return score

    def make_move(self, dice: List[int]):
        """
        Makes a move for the AI player.

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
