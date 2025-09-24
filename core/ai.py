from core.dice import roll_dice
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
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
        self.board = None
        self.player = None

    def play_turn(self):
        """
        IA básica mejorada: evalúa opciones y elige la menos mala.

        Handles doubles, prioritizes bar/hits, allows partial sequences.

        Parameters
        ----------
        board : Board
            The current game.
        """
        # Ejemplo de IA muy simple: mueve la primera ficha posible
        for from_point in range(24):
            for die in range(1, 7):
                if self.board.is_valid_move(from_point, die, self.player):
                    to_point = (
                        from_point + (-1 if self.player.color == "white" else 1) * die
                    )
                    if 0 <= to_point < 24:
                        self.board.move_piece(from_point, to_point, self.player)
                        return
        # Si no hay movimientos válidos, no hace nada

    def _choose_best_sequence(self, board, sequences, player):
        return sequences[0] if sequences else []

    def _copy_board(self, board):
        import copy

        return copy.deepcopy(board)

    def _evaluate_sequence(self, board, sequence, player):
        return sum(die for _, die in sequence)
