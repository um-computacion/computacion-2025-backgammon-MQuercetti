import unittest  # Agrega esta línea
from unittest.mock import patch
from core.player import Player
from core.checkers import Checkers
from core.board import Board, roll_dice


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.p1 = Player("Alice", "white")
        self.p2 = Player("Bob", "black")
        self.board = Board(self.p1, self.p2, random_positions=False)
        self.board.set_ai(self.board.__ai__)  # Usa setter para asignar AI

    def test_init(self):
        """Test initialization: Players, points, bar, off_board."""
        self.assertEqual(self.board.get_player1(), self.p1)
        self.assertEqual(self.board.get_player2(), self.p2)
        self.assertIsNone(self.board.__winner__)
        self.assertEqual(self.board.get_current_player(), self.p1)
        self.assertEqual(len(self.board.get_points()), 24)
        self.assertEqual(len(self.board.get_points()[23]), 2)  # White start
        self.assertEqual(len(self.board.get_points()[0]), 2)  # Black start
        self.assertEqual(self.board.get_bar()[self.p1], [])
        self.assertEqual(self.board.get_bar()[self.p2], [])
        self.assertEqual(self.board.__off_board__[self.p1], 0)
        self.assertEqual(self.board.__off_board__[self.p2], 0)

    def test_get_point(self):
        """Test getting point checkers."""
        point = self.board.get_point(23)
        self.assertEqual(len(point), 2)
        self.assertEqual(point[0].get_owner(), self.p1)  # Usa getter

    def test_switch_player(self):
        """Test switching current player."""
        self.assertEqual(self.board.get_current_player(), self.p1)
        self.board.switch_player()
        self.assertEqual(self.board.get_current_player(), self.p2)

    def test_is_valid_move_normal_white(self):
        """Test valid move for white from start (no bar)."""
        self.assertTrue(self.board.is_valid_move(23, 1, self.p1))

    def test_is_valid_move_blocked(self):
        """Test invalid: Blocked by 2+ opponents."""
        # Setup: Put 2 blacks on point 22
        self.board.set_point(22, [Checkers(self.p2), Checkers(self.p2)])  # Usa setter
        self.assertFalse(self.board.is_valid_move(23, 1, self.p1))  # 23 to 22 blocked

    def test_is_valid_move_bar_priority_white(self):
        """Test bar priority: Must move from bar first."""
        # Put white on bar
        self.board.add_to_bar(self.p1, Checkers(self.p1))  # Usa setter
        self.assertFalse(self.board.is_valid_move(23, 1, self.p1))  # Can't move from 23
        self.assertTrue(self.board.is_valid_move(-1, 2, self.p1))  # Must move from bar with die=2 (to point 1, empty)

    def test_move_piece_normal(self):
        """Test normal move: From start, no hit."""
        initial_23 = len(self.board.get_points()[23])
        initial_22 = len(self.board.get_points()[22])
        self.board.move_piece(23, 1, self.p1)
        self.assertEqual(len(self.board.get_points()[23]), initial_23 - 1)
        self.assertEqual(len(self.board.get_points()[22]), initial_22 + 1)

    def test_move_piece_hit(self):
        """Test hit: Send single opponent to bar."""
        # Put 1 black on 22
        self.board.set_point(22, [Checkers(self.p2)])  # Usa setter
        initial_bar_black = len(self.board.get_bar()[self.p2])
        self.board.move_piece(23, 1, self.p1)
        self.assertEqual(len(self.board.get_points()[22]), 1)  # White now on 22
        self.assertEqual(len(self.board.get_bar()[self.p2]), initial_bar_black + 1)  # Black hit

    def test_move_piece_bear_off(self):
        """Test bear-off: When all in home, move off-board."""
        # Move all whites to home (points 0-5 for white)
        for i in range(24):
            self.board.set_point(i, [])  # Usa setter para limpiar
        self.board.set_point(0, [Checkers(self.p1)])  # Usa setter
        self.board.move_piece(0, 1, self.p1)  # Bear-off
        self.assertEqual(self.board.__off_board__[self.p1], 1)

    @patch('core.board.roll_dice')
    def test_ai_play_turn(self, mock_roll):
        """Test integrated AI: Rolls and moves (mock random)."""
        mock_roll.return_value = [3, 4]
        initial_0 = len(self.board.get_points()[0])
        self.board.__ai__.play_turn([3, 4])  # Mantengo acceso directo para AI
        # AI should have moved if possible
        self.assertLess(len(self.board.get_points()[0]), initial_0)  # Moved

    def test_roll_dice(self):
        """Test dice rolling."""
        dice = self.board.roll_dice()
        self.assertIsInstance(dice, list)
        self.assertEqual(len(dice), 2)
        for d in dice:
            self.assertIn(d, range(1, 7))


if __name__ == "__main__":
    unittest.main()
