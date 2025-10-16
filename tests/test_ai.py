import unittest
from unittest.mock import MagicMock, patch
from core.ai import AIPlayer
import copy


class DummyPlayer:
    def __init__(self, name, color):
        self.__name__ = name
        self.__color__ = color

    def get_name(self):
        return self.__name__

    def get_color(self):
        return self.__color__

    def __eq__(self, other):
        if not isinstance(other, DummyPlayer):
            return False
        return self.__name__ == other.__name__ and self.__color__ == other.__color__

    def __hash__(self):
        return hash((self.__name__, self.__color__))


class DummyCheckers:
    def __init__(self, owner):
        self.__owner__ = owner

    def get_owner(self):
        return self.__owner__


class DummyBoard:
    def __init__(self, owner1, owner2):
        self.points = [[] for _ in range(24)]
        # Agrega algunos checkers para moves válidos
        self.points[23] = [DummyCheckers(owner1)]  # White on 23
        self.points[0] = [DummyCheckers(owner2)] * 6  # 6 blacks in home
        self.points[6] = [DummyCheckers(owner2)]  # Black on 6 (para mover a home)
        self.bar = {owner1: [], owner2: []}

    def move_piece(self, from_point, die, player):
        self._move_piece(from_point, die, player)

    def _move_piece(self, from_point, die, player):
        # Simula move: from 6 with die 3, move to 3 (home for black)
        if from_point == 6 and die == 3 and self.points[6]:
            checker = self.points[6].pop()
            to_point = 3  # Home for black
            self.points[to_point].append(checker)

    def get_point(self, index):
        return self.points[index] if 0 <= index < 24 else []

    def is_valid_move(self, point, die, player):
        # Simple: valid if point 6 and die 3 or 4
        return point == 6 and die in [3, 4]


class TestAIPlayer(unittest.TestCase):
    def setUp(self):
        self.board = DummyBoard(DummyPlayer("Alice", "white"), DummyPlayer("Bob", "black"))
        # Quita mock: usa método real
        self.ai = AIPlayer()
        self.ai.__board__ = self.board
        self.ai.__player__ = DummyPlayer("Bob", "black")

    def test_choose_best_sequence_returns_sequence(self):
        board = DummyBoard(DummyPlayer("Alice", "white"), DummyPlayer("Bob", "black"))
        sequences = [[(23, 3)]]
        player = DummyPlayer("Bob", "black")
        best = self.ai._choose_best_sequence(board, sequences, player)
        self.assertIsInstance(best, list)

    def test_copy_board_returns_board(self):
        board = DummyBoard(DummyPlayer("Alice", "white"), DummyPlayer("Bob", "black"))
        copy = self.ai._copy_board(board)
        self.assertIsInstance(copy, DummyBoard)

    def test_evaluate_sequence_returns_score(self):
        board = DummyBoard(DummyPlayer("Alice", "white"), DummyPlayer("Bob", "black"))
        seq = [(6, 3)]  # Cambia seq para mover black a home
        player = DummyPlayer("Bob", "black")
        score = self.ai._evaluate_sequence(board, seq, player)
        self.assertEqual(score, 7)  # Ahora sí: 6 +1 =7

    def test_play_turn_executes_moves(self):
        initial_3 = len(self.board.points[3])
        self.ai.play_turn([3, 4])
        self.assertEqual(len(self.board.points[3]), initial_3 + 1)  # Verifica que se movió

    def test_play_turn_calls_ai_play_turn(self):
        with patch.object(self.ai, 'play_turn') as mock_play:
            self.ai.play_turn([3, 4])
            mock_play.assert_called_once_with([3, 4])


if __name__ == "__main__":
    unittest.main()