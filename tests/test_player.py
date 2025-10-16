import unittest
from core.player import Player
from core.board import Board


class TestPlayer(unittest.TestCase):
    """
    Tests for the Player class.
    """

    def setUp(self):
        self.p1 = Player("Alice", "white")
        self.p2 = Player("Bob", "black")
        self.board = Board(self.p1, self.p2)

    def test_init(self):
        """Test initialization: name and color set correctly."""
        self.assertEqual(self.p1.get_name(), "Alice")  # Usa getter
        self.assertEqual(self.p1.get_color(), "white")  # Usa getter
        self.assertEqual(self.p2.get_name(), "Bob")  # Usa getter
        self.assertEqual(self.p2.get_color(), "black")  # Usa getter

    def test_eq_same_name(self):
        """Test equality: Same name, different color → True."""
        p3 = Player("Alice", "black")
        self.assertEqual(self.p1, p3)

    def test_eq_different_name(self):
        """Test inequality: Different names → False."""
        p3 = Player("Charlie", "white")
        self.assertNotEqual(self.p1, p3)

    def test_eq_non_player(self):
        """Test with non-Player object → False."""
        self.assertNotEqual(self.p1, "not a player")

    def test_repr(self):
        """Test string representation."""
        self.assertEqual(repr(self.p1), "Player(name='Alice', color='white')")

    def test_player_equality(self):
        """Test player equality."""
        p3 = Player("Alice", "white")
        self.assertEqual(self.p1, p3)

    def test_turno(self):
        """Test if the current player's name is displayed correctly."""
        self.assertEqual(f"Turno: {self.p2.get_name()}", "Turno: Bob")  # Usa getter


if __name__ == "__main__":
    unittest.main()
