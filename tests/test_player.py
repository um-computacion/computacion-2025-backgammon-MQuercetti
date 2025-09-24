import unittest
from core.player import Player
from core.board import Board  # Asegúrate de que esto apunte a la ubicación correcta


class TestPlayer(unittest.TestCase):
    """
    Tests for the Player class.
    """

    def setUp(self):
        self.p1 = Player("Alice", "white")
        self.p2 = Player("Bob", "black")
        board = Board(self.p1, self.p2)

    def test_init(self):
        """Test initialization: name and color set correctly."""
        self.assertEqual(self.p1.name, "Alice")
        self.assertEqual(self.p1.color, "white")
        self.assertEqual(self.p2.color, "black")

    def test_repr(self):
        """Test string representation."""
        self.assertIn("Bob", repr(self.p2))

    def test_eq_same_name(self):
        """Test equality: Same name, different color → True."""
        same_name_player = Player("Alice", "black")
        self.assertEqual(self.p1, same_name_player)

    def test_eq_different_name(self):
        """Test inequality: Different names → False."""
        self.assertNotEqual(self.p1, self.p2)

    def test_eq_non_player(self):
        """Test with non-Player object → False."""
        self.assertNotEqual(self.p1, "not a player")

    def test_player_equality(self):
        p1 = Player("Carol", "white")
        p2 = Player("Carol", "white")
        self.assertEqual(p1, p2)

    def test_turno(self):
        """Test if the current player's name is displayed correctly."""
        self.assertEqual(f"Turno: {self.p1.name}", "Turno: Alice")
        self.assertEqual(f"Turno: {self.p2.name}", "Turno: Bob")


if __name__ == "__main__":
    unittest.main()
