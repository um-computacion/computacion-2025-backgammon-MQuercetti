import unittest
from core.player import Player
from core.checkers import Checkers
from core.board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        # White moves from high to low indices (home: 0-5)
        # Black moves from low to high indices (home: 18-23)
        self.p1 = Player("Alice", "white") 
        self.p2 = Player("Bob", "black")   
        self.board = Board(self.p1, self.p2, random_positions=False)

    def test_initial_setup(self):
        # White's checkers
        self.assertEqual(len(self.board.get_point(23)), 2)
        self.assertEqual(self.board.get_point(23)[0].get_owner(), self.p1)
        self.assertEqual(len(self.board.get_point(5)), 5)
        self.assertEqual(self.board.get_point(5)[0].get_owner(), self.p1)
        # Black's checkers
        self.assertEqual(len(self.board.get_point(0)), 2)
        self.assertEqual(self.board.get_point(0)[0].get_owner(), self.p2)
        self.assertEqual(len(self.board.get_point(18)), 5)
        self.assertEqual(self.board.get_point(18)[0].get_owner(), self.p2)

    def test_white_move_direction(self):
        # From point 23 with a die of 2 should land on 21.
        self.assertTrue(self.board.is_valid_move(23, 2, self.p1))
        # Moving backwards is not allowed.
        self.assertFalse(self.board.is_valid_move(12, -3, self.p1))
        # A move from 5 with a die of 3 lands on 2.
        self.assertTrue(self.board.is_valid_move(5, 3, self.p1))

    def test_black_move_direction(self):
        # From point 0 with a die of 2 should land on 2.
        self.assertTrue(self.board.is_valid_move(0, 2, self.p2))
        # Moving backwards is not allowed.
        self.assertFalse(self.board.is_valid_move(11, -3, self.p2))
        # A move from 18 with a die of 3 lands on 21.
        self.assertTrue(self.board.is_valid_move(18, 3, self.p2))

    def test_can_bear_off_white(self):
        # Clear the board
        for i in range(24): self.board.get_points()[i] = []
        # Place all 15 checkers in white's home board
        self.board.get_points()[0] = [Checkers(self.p1) for _ in range(5)]
        self.board.get_points()[1] = [Checkers(self.p1) for _ in range(5)]
        self.board.get_points()[2] = [Checkers(self.p1) for _ in range(5)]
        self.assertTrue(self.board.can_player_bear_off(self.p1))
        
        # Add one checker outside the home board
        self.board.get_points()[10] = [Checkers(self.p1)]
        self.board.get_points()[2][0] = Checkers(self.p2) # Change owner to avoid having > 15 checkers
        self.assertFalse(self.board.can_player_bear_off(self.p1))
        
    def test_can_bear_off_black(self):
        # Clear the board
        for i in range(24): self.board.get_points()[i] = []
        # Place all 15 checkers in black's home board
        self.board.get_points()[18] = [Checkers(self.p2) for _ in range(5)]
        self.board.get_points()[19] = [Checkers(self.p2) for _ in range(5)]
        self.board.get_points()[20] = [Checkers(self.p2) for _ in range(5)]
        self.assertTrue(self.board.can_player_bear_off(self.p2))
        
        # Add one checker outside the home board
        self.board.get_points()[10] = [Checkers(self.p2)]
        self.board.get_points()[20][0] = Checkers(self.p1)
        self.assertFalse(self.board.can_player_bear_off(self.p2))

    def test_bear_off_white_exact_die(self):
        for i in range(24): self.board.get_points()[i] = []
        self.board._set_off_board_count(self.p1, 14)
        self.board.get_points()[5] = [Checkers(self.p1)] # A checker on the 6-point
        # A roll of 6 is required to bear off from the 6-point (index 5).
        self.assertTrue(self.board.is_valid_bear_off_move(5, 6, self.p1))
        self.assertFalse(self.board.is_valid_bear_off_move(5, 5, self.p1))
        
    def test_bear_off_white_overshoot_not_allowed(self):
        for i in range(24): self.board.get_points()[i] = []
        self.board._set_off_board_count(self.p1, 14)
        self.board.get_points()[3] = [Checkers(self.p1)] # A checker on the 4-point
        # A roll of 5 or 6 is NOT allowed because it's not an exact roll.
        self.assertFalse(self.board.is_valid_bear_off_move(3, 5, self.p1))
        self.assertFalse(self.board.is_valid_bear_off_move(3, 6, self.p1))

    def test_bear_off_black_exact_die(self):
        for i in range(24): self.board.get_points()[i] = []
        self.board._set_off_board_count(self.p2, 14)
        self.board.get_points()[18] = [Checkers(self.p2)] # Black's 6-point
        # A roll of 6 is needed to bear off from point 18 (24 - 18 = 6).
        self.assertTrue(self.board.is_valid_bear_off_move(18, 6, self.p2))
        self.assertFalse(self.board.is_valid_bear_off_move(18, 5, self.p2))

    def test_bear_off_black_overshoot_not_allowed(self):
        for i in range(24): self.board.get_points()[i] = []
        self.board._set_off_board_count(self.p2, 14)
        self.board.get_points()[20] = [Checkers(self.p2)] # Black's 4-point
        # A roll of 5 is NOT allowed.
        self.assertFalse(self.board.is_valid_bear_off_move(20, 5, self.p2))

if __name__ == "__main__":
    unittest.main()
