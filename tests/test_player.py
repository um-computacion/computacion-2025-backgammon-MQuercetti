import unittest
from unittest.mock import patch
from core.game import Game
from core.player import Player
from core.ai import AIPlayer

class TestGame(unittest.TestCase):

    def setUp(self):
        """Set up a new game for each test."""
        self.p1 = Player("Human", "white")
        # The AIPlayer is not a Player subclass, it's a controller. 
        # The game needs a Player instance for the AI.
        self.p2 = Player("Computer", "black") 
        self.game = Game(players=[self.p1, self.p2])

    def test_game_initialization(self):
        """Test that the game initializes correctly."""
        self.assertEqual(len(self.game.players), 2)
        self.assertIn(self.p1, self.game.players)
        self.assertIn(self.p2, self.game.players)
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.dice)
        self.assertIsNone(self.game.initial_roll_winner)

    def test_switch_player(self):
        """Test that the player turn switches correctly."""
        initial_player = self.game.current_player
        self.game.switch_player()
        next_player = self.game.current_player
        self.assertNotEqual(initial_player, next_player)
        self.game.switch_player()
        self.assertEqual(self.game.current_player, initial_player)

    @patch('core.dice.Dice.roll_one', side_effect=[6, 1])
    def test_determine_first_player_p1_wins(self, mock_roll):
        """Test the first player determination when player 1 rolls higher."""
        self.game.determine_first_player()
        self.assertEqual(self.game.initial_roll_winner, self.p1)
        self.assertEqual(self.game.current_player, self.p1)
        # The dice values from the initial roll should be set for the first turn
        self.assertEqual(self.game.dice.get_values(), [6, 1])

    @patch('core.dice.Dice.roll_one', side_effect=[2, 5])
    def test_determine_first_player_p2_wins(self, mock_roll):
        """Test the first player determination when player 2 rolls higher."""
        self.game.determine_first_player()
        self.assertEqual(self.game.initial_roll_winner, self.p2)
        self.assertEqual(self.game.current_player, self.p2)
        self.assertEqual(self.game.dice.get_values(), [2, 5])

    @patch('core.dice.Dice.roll_one', side_effect=[3, 3, 5, 2])
    def test_determine_first_player_tie(self, mock_roll):
        """Test that a tie in the initial roll leads to a re-roll."""
        self.game.determine_first_player()
        self.assertEqual(self.game.initial_roll_winner, self.p1)
        self.assertEqual(self.game.current_player, self.p1)
        # Check that it took two sets of rolls
        self.assertEqual(mock_roll.call_count, 4)
        self.assertEqual(self.game.dice.get_values(), [5, 2])
        
    def test_is_game_over(self):
        """Test the game-over condition."""
        # Initially, game is not over
        self.assertFalse(self.game.is_game_over())
        
        # Simulate one player bearing off all checkers
        with patch.object(self.game.board, 'is_game_over', return_value=True):
            self.assertTrue(self.game.is_game_over())

if __name__ == '__main__':
    unittest.main()
