from core.dice import roll_dice
import random
import copy


class AIPlayer:
    def __init__(self, name="Computer"):
        self.name = name

    def play_turn(self, board, player):
        """IA básica mejorada: evalúa opciones y elige la menos mala."""
        d1, d2 = roll_dice()
        print(f"{self.name} rolled: {d1}, {d2}")

        possible_sequences = self._get_possible_sequences(board, [d1, d2], player)

        if not possible_sequences:
            print(f"{self.name} has no valid moves")
            return

        chosen_sequence = self._choose_best_sequence(board, possible_sequences, player)

        for from_point, die in chosen_sequence:
            board.move_piece(from_point, die, player)
            print(f"{self.name} moved from {from_point} with {die}")

    def _get_possible_sequences(self, board, dice, player):
        """Genera todas las secuencias válidas de movimientos."""
        sequences = []
        for dice_order in [dice, dice[::-1]]:
            sequence = []
            temp_board = self._copy_board(board)
            for die in dice_order:
                moved = False
                for i, point in enumerate(temp_board.points):
                    if point and point[0].owner == player:
                        if temp_board.is_valid_move(i, die, player):
                            temp_board.move_piece(i, die, player)
                            sequence.append((i, die))
                            moved = True
                            break
                if not moved:
                    break
            if len(sequence) == len(dice_order):
                sequences.append(sequence)
        return sequences

    def _choose_best_sequence(self, board, sequences, player):
        """Elige la mejor secuencia según una evaluación simple."""
        if not sequences:
            return []
        # Evaluar cada secuencia y elegir la mejor
        return max(
            sequences, key=lambda seq: self._evaluate_sequence(board, seq, player)
        )

    def _evaluate_sequence(self, board, sequence, player):
        """
        Evalúa una secuencia de movimientos.
        Suma la cantidad de fichas movidas hacia la zona de salida como criterio simple.
        """
        score = 0
        temp_board = self._copy_board(board)
        for from_point, die in sequence:
            if temp_board.is_valid_move(from_point, die, player):
                temp_board.move_piece(from_point, die, player)
                # Ejemplo: sumar puntos si la ficha se acerca al final
                score += die
        return score

    def _copy_board(self, board):
        """
        Crea una copia profunda del tablero para simulaciones.
        """
        return copy.deepcopy(board)
