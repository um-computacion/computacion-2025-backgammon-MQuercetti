import unittest
from unittest.mock import MagicMock, patch
from core.ai import AIPlayer
import copy

class DummyPlayer:
    def __init__(self, name, color="white"):
        self.name = name
        self.color = color


class DummyBoard:
    def __init__(self, player1, player2):  # Pasa players al constructor
        self.bar = {player1: [], player2: []}  # Usa los mismos objetos
        self.points = [[] for _ in range(24)]
        self.is_valid_move = MagicMock(return_value=True)
        self.move_piece = MagicMock()  # Agrega move_piece como mock

    def __deepcopy__(self, memo):
        # Crea una copia con los mismos players (usa self.bar.keys())
        players = list(self.bar.keys())
        new_board = DummyBoard(players[0], players[1])
        new_board.bar = copy.deepcopy(self.bar, memo)
        new_board.points = copy.deepcopy(self.points, memo)
        new_board.is_valid_move = self.is_valid_move
        new_board.move_piece = self.move_piece
        return new_board


class TestAIPlayer(unittest.TestCase):
    @patch("core.board.roll_dice", return_value=(3, 4))
    def test_play_turn_executes_moves(self, mock_roll):
        ai = AIPlayer()
        player1 = DummyPlayer("Alice", "white")
        player2 = DummyPlayer("Bob", "black")
        board = DummyBoard(player1, player2)
        player = DummyPlayer("AI")
        ai.board = board  # Asignar antes de llamar
        ai.player = player1  # O el que uses
        ai.play_turn([3, 4])  # Pasa dados
        self.assertTrue(board.move_piece.called)

    def test_choose_best_sequence_returns_sequence(self):
        ai = AIPlayer()
        board = DummyBoard(DummyPlayer("Alice", "white"), DummyPlayer("Bob", "black"))
        player = DummyPlayer("AI")
        sequences = [[(0, 3), (1, 4)], [(2, 4), (3, 3)]]
        best = ai._choose_best_sequence(board, sequences, player)
        self.assertIn(best, sequences)

    def test_evaluate_sequence_returns_score(self):
        ai = AIPlayer()
        board = DummyBoard(DummyPlayer("Alice", "white"), DummyPlayer("Bob", "black"))
        player = DummyPlayer("AI")
        seq = [(0, 3), (1, 4)]
        score = ai._evaluate_sequence(board, seq, player)
        self.assertEqual(score, 7)

    def test_copy_board_returns_board(self):
        ai = AIPlayer()
        board = DummyBoard(DummyPlayer("Alice", "white"), DummyPlayer("Bob", "black"))
        copy_board = ai._copy_board(board)
        self.assertIsInstance(copy_board, DummyBoard)

    def test_play_turn_calls_ai_play_turn(self):
        ai = AIPlayer()
        player1 = DummyPlayer("Alice", "white")
        player2 = DummyPlayer("Bob", "black")
        board = DummyBoard(player1, player2)
        ai.board = board
        ai.player = player1
        # Solo verifica que no lanza excepción y acepta ambos argumentos
        try:
            ai.play_turn([3, 4])  # Pasa dados
        except Exception as e:
            self.fail(f"ai.play_turn() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
