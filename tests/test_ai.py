import unittest
from unittest.mock import MagicMock, patch
from core.ai import AIPlayer


class DummyPlayer:
    def __init__(self, name, color="white"):
        self.name = name
        self.color = color


class DummyBoard:
    def __init__(self):
        self.points = [[MagicMock(owner=DummyPlayer("AI"))] for _ in range(24)]
        self.move_piece = MagicMock()
        self.is_valid_move = MagicMock(return_value=True)

    def __deepcopy__(self, memo):
        new_board = DummyBoard()
        new_board.points = [list(point) for point in self.points]
        new_board.move_piece = MagicMock()
        new_board.is_valid_move = MagicMock(return_value=True)
        return new_board


class TestAIPlayer(unittest.TestCase):
    @patch("core.board.roll_dice", return_value=(3, 4))
    def test_play_turn_executes_moves(self, mock_roll):
        ai = AIPlayer()
        board = DummyBoard()
        player = DummyPlayer("AI")
        ai.board = board  # Asignar antes de llamar
        ai.player = player
        ai.play_turn()  # Sin argumentos
        self.assertTrue(board.move_piece.called)

    def test_choose_best_sequence_returns_sequence(self):
        ai = AIPlayer()
        board = DummyBoard()
        player = DummyPlayer("AI")
        sequences = [[(0, 3), (1, 4)], [(2, 4), (3, 3)]]
        best = ai._choose_best_sequence(board, sequences, player)
        self.assertIn(best, sequences)

    def test_evaluate_sequence_returns_score(self):
        ai = AIPlayer()
        board = DummyBoard()
        player = DummyPlayer("AI")
        seq = [(0, 3), (1, 4)]
        score = ai._evaluate_sequence(board, seq, player)
        self.assertEqual(score, 7)

    def test_copy_board_returns_board(self):
        ai = AIPlayer()
        board = DummyBoard()
        copy_board = ai._copy_board(board)
        self.assertIsInstance(copy_board, DummyBoard)

    def test_play_turn_calls_ai_play_turn(self):
        ai = AIPlayer()
        board = DummyBoard()
        player = DummyPlayer("AI")
        ai.board = board
        ai.player = player
        # Solo verifica que no lanza excepción y acepta ambos argumentos
        try:
            ai.play_turn()  # Sin argumentos
        except Exception as e:
            self.fail(f"ai.play_turn() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
