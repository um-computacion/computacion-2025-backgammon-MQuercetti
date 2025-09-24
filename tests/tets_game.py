import unittest
from unittest.mock import patch, MagicMock
from core.player import Player
from core.board import Board
from core.ai import AIPlayer
from core.game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.human = Player("Human", "white")
        self.ai = AIPlayer("Computer")
        self.board = Board(self.human, Player("AI", "black"))
        self.game = Game()
        self.game.board = self.board
        self.game.human = self.human
        self.game.ai_player = self.ai

    def test_game_initialization(self):
        self.assertIsInstance(self.game.board, Board)
        self.assertIsInstance(self.game.human, Player)
        self.assertIsInstance(self.game.ai_player, AIPlayer)

    @patch("builtins.input", return_value="0 1")
    @patch.object(Board, "move_checker")
    def test_human_turn(self, mock_move, mock_input):
        # Simula un turno humano y verifica que se intente mover una ficha
        self.game.human_turn()
        self.assertTrue(mock_move.called)

    @patch.object(AIPlayer, "play_turn")
    def test_ai_turn(self, mock_ai_play):
        # Simula un turno de la IA y verifica que se llame play_turn
        self.game.ai_turn()
        self.assertTrue(mock_ai_play.called)

    @patch.object(Game, "is_game_over", return_value=True)
    def test_play_game_over(self, mock_game_over):
        # Simula que el juego termina inmediatamente
        with patch.object(self.game, "human_turn") as mock_human, patch.object(
            self.game, "ai_turn"
        ) as mock_ai:
            self.game.play()
            self.assertFalse(mock_human.called or mock_ai.called)


if __name__ == "__main__":
    unittest.main()
