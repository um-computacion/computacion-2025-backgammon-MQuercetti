from core.dice import roll_dice
import random
import copy
from typing import List, Tuple, Any
from core.board import Board

class AIPlayer:
    """
    A class used to represent an AI player in the Backgammon game.

    Attributes
    ----------
    name : str
        The name of the AI player (default "Computer").

    Methods
    -------
    play_turn(board, player)
        Executes the AI's turn: rolls dice, generates possible sequences, evaluates and applies the best.
    """

    def __init__(self, name: str = "Computer"):
        """
        Parameters
        ----------
        name : str, optional
            The name of the AI player (default "Computer").
        """
        self.name = name

    def play_turn(self, board: Board, player: Any):
        """
        IA básica mejorada: evalúa opciones y elige la menos mala.

        Handles doubles, prioritizes bar/hits, allows partial sequences.

        Parameters
        ----------
        board : Board
            The current game. 
            """
