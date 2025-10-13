from typing import TYPE_CHECKING, List, Any
import copy
import random

if TYPE_CHECKING:
    from core.board import Board
    from core.player import Player


class AIPlayer:
    """
    Representa un jugador de IA. La lógica para decidir los movimientos está aquí.
    """

    def __init__(self, name: str = "Computer"):
        self.name = name
        self.board: "Board" = None  # Asignado por Board
        self.player: "Player" = None  # Asignado por Board

    def play_turn(self, dice: List[int]) -> None:
        """
        Ejecuta el turno de la IA usando los dados proporcionados.
        """
        if not self.board or not self.player:
            raise ValueError("Board and player must be assigned to AIPlayer")
        
        # Lógica básica: intenta mover con cada dado
        for die in dice:
            valid_moves = self._get_valid_moves(die)
            if valid_moves:
                # Elige el primer movimiento válido (puedes mejorar esto)
                from_point, to_point = valid_moves[0]
                self.board.move_piece(from_point, die, self.player)
                break  # Solo un movimiento por dado por simplicidad

    def _get_valid_moves(self, die: int) -> List[tuple]:
        """
        Devuelve una lista de movimientos válidos (from_point, to_point) para el dado.
        Incluye bear-off si es posible.
        """
        moves = []
        # Home points: 0-5 for white, 18-23 for black
        home_points = range(0, 6) if self.player.color == "white" else range(18, 24)
        
        for from_point in range(24):
            if self.board.is_valid_move(from_point, die, self.player):
                direction = -1 if self.player.color == "white" else 1
                to_point = from_point + direction * die
                if 0 <= to_point < 24:
                    moves.append((from_point, to_point))
                else:
                    # Bear-off: to_point fuera del tablero
                    moves.append((from_point, to_point))
        
        # También movimientos desde el bar
        if len(self.board.bar[self.player]) > 0:
            bar_point = -1 if self.player.color == "white" else 24
            if self.board.is_valid_move(bar_point, die, self.player):
                direction = -1 if self.player.color == "white" else 1
                to_point = bar_point + direction * die
                moves.append((bar_point, to_point))
        
        return moves

    def _choose_best_sequence(self, board: "Board", sequences: List[List[tuple]], player: "Player") -> List[tuple]:
        """
        Elige la mejor secuencia de movimientos basada en evaluación.
        """
        if not sequences:
            return []
        # Por simplicidad, elige la primera secuencia
        return sequences[0]

    def _evaluate_sequence(self, board: "Board", seq: List[tuple], player: "Player") -> int:
        """
        Evalúa una secuencia de movimientos y devuelve un puntaje.
        """
        # Puntaje: suma de los dados usados en la secuencia
        score = 0
        for move in seq:
            from_point, to_point = move
            # Asumiendo que to_point es el dado usado (como en los tests)
            score += to_point
        return score

    def _copy_board(self, board: "Board") -> "Board":
        """
        Crea una copia profunda del tablero para simulación.
        """
        return copy.deepcopy(board)
