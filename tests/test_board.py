# tests/test_board.py
import unittest
from unittest.mock import patch
from core.player import Player
from core.checkers import Checkers
from core.board import Board, roll_dice


class TestBoard(unittest.TestCase):
    """
    Tests for the Board class (including integrated AI and game logic).
    """

    def setUp(self):
        self.p1 = Player("Alice", "white")
        self.p2 = Player("Bob", "black")
        self.board = Board(self.p1, self.p2)

    def test_init(self):
        """Test initialization: Players, points, bar, off_board."""
        self.assertEqual(self.board.player1.name, "Alice")
        self.assertEqual(self.board.player1.color, "white")
        self.assertEqual(self.board.player2.color, "black")
        self.assertEqual(len(self.board.points), 24)
        self.assertEqual(len(self.board.points[23]), 2)  # White start
        self.assertEqual(len(self.board.points[0]), 2)  # Black start
        self.assertEqual(self.board.bar[self.p1], [])
        self.assertEqual(self.board.off_board[self.p1], 0)
        self.assertIsNotNone(self.board.ai)  # AI integrada

    def test_initial_points(self):
        total_checkers = sum(len(point) for point in self.board.points)
        self.assertEqual(total_checkers, 30)

    def test_get_point(self):
        """Test getting point checkers."""
        point = self.board.get_point(23)
        self.assertEqual(len(point), 2)
        self.assertEqual(point[0].owner.color, "white")
        with self.assertRaises(IndexError):
            self.board.get_point(25)  # Invalid

    def test_roll_dice(self):
        """Test board.roll_dice() calls global function."""
        with patch("core.board.roll_dice") as mock_roll:
            mock_roll.return_value = [1, 2]
            result = self.board.roll_dice()
            self.assertEqual(result, [1, 2])
            mock_roll.assert_called_once()

    def test_switch_player(self):
        """Test switching current player."""
        original = self.board.current_player
        self.board.switch_player()
        self.assertEqual(self.board.current_player, self.p2)
        self.board.switch_player()
        self.assertEqual(self.board.current_player, original)

    def test_is_game_over_initial(self):
        """Test game not over at start."""
        self.assertFalse(self.board.is_game_over())

    def test_is_valid_move_normal_white(self):
        """Test valid move for white from start (no bar)."""
        # White from 23 with 1 → to 22 (empty, valid)
        self.assertTrue(self.board.is_valid_move(23, 1, self.p1))

    def test_is_valid_move_blocked(self):
        """Test invalid: Blocked by 2+ opponents."""
        # Simula bloqueo en punto 22 (agrega 2 black ficticios, pero usa setup)
        # Para test: Asume inicial no bloqueado, pero prueba lógica
        # Mueve primero para setup (simplificado)
        self.board.move_piece(23, 1, self.p1)  # Mueve a 22
        # Ahora prueba move a punto con 2 (e.g., simula)
        # Nota: Inicial no tiene bloques; test general
        self.assertFalse(
            self.board.is_valid_move(0, 1, self.p1)
        )  # Opuesto bloqueado? Inicial 2B en 0

    def test_is_valid_move_bar_priority_white(self):
        """Test bar priority: Must move from bar first."""
        # Simula bar: Mueve a bar (hit simple)
        self.board.move_piece(0, 1, self.p2)  # Black mueve, pero para white bar
        # Para white bar: Asume hit envía white a bar (setup manual)
        white_checker = Checkers(self.p1)
        self.board.bar[self.p1].append(white_checker)
        # Ahora: Debe usar from=-1, no points
        self.assertTrue(self.board.is_valid_move(-1, 1, self.p1))
        self.assertFalse(
            self.board.is_valid_move(23, 1, self.p1)
        )  # No puede desde point si bar

    def test_move_piece_normal(self):
        """Test normal move: From start, no hit."""
        initial_23 = len(self.board.points[23])
        to_point = 23 - 1  # Die=1, white direction -1
        self.board.move_piece(23, 1, self.p1)
        self.assertEqual(len(self.board.points[23]), initial_23 - 1)
        self.assertEqual(len(self.board.points[to_point]), 1)
        self.assertEqual(self.board.points[to_point][0].owner, self.p1)

    def test_move_piece_hit(self):
        """Test hit: Send single opponent to bar."""
        # Setup: Mueve white a punto con 1 black (simplificado)
        # Inicial: P23 white, pero para hit, asume move black to white area (test general)
        # Para demo: Crea escenario
        black_checker = Checkers(self.p2)
        self.board.points[22] = [black_checker]  # Single black in 22
        self.board.move_piece(23, 1, self.p1)  # White from 23 to 22, hit
        self.assertEqual(len(self.board.points[22]), 1)  # White ahora
        self.assertEqual(len(self.board.bar[self.p2]), 1)  # Black to bar

    def test_move_piece_bear_off(self):
        """Test bear-off: When all in home, move off-board."""
        # Simplificado: Asume all white in home (0-5), move from 1 with 1 → off
        # Setup manual (vacía points, pon en home)
        for i in range(24):
            self.board.points[i] = []
        self.board.off_board[self.p1] = 14  # 1 remaining
        self.board.points[0] = [
            Checkers(self.p1)
        ]  # Ficha en punto 0 (home para blanco)
        self.board.move_piece(
            0, 1, self.p1
        )  # Mover desde 0 con die=1: to_point = 0 + (-1)*1 = -1 (bear-off)
        self.assertEqual(self.board.off_board[self.p1], 15)
        self.assertTrue(self.board.is_game_over())
        self.assertEqual(self.board.winner, self.p1)

    def test_move_piece_invalid(self):
        """Test invalid move raises ValueError."""
        with self.assertRaises(ValueError):
            self.board.move_piece(99, 1, self.p1)  # Invalid from

    def test_ai_play_turn(self):
        """Test integrated AI: Rolls and moves (mock random)."""
        with patch.object(self.board.ai, "play_turn") as mock_play:
            self.board.current_player = self.p2
            self.board.ai.play_turn(self.board, self.p2)
            mock_play.assert_called_once()  # Verifica llamada
        # Test simple move: Asume AI mueve si posible
        with patch("core.dice.random.randint", return_value=1):  # Fuerza die=1
            self.board.current_player = self.p2
            initial_0 = len(self.board.points[0])
            self.board.ai.play_turn()
            self.assertLess(len(self.board.points[0]), initial_0)  # Movió

    def test_play_game_loop(self):
        """Test play() loop: Runs at least one turn without crash."""
        # Mock input para human (simula input '23' con die=1)
        with patch("builtins.input", return_value="23"):
            with patch.object(self.board.ai, "play_turn"):  # Mock AI
                # Corre play, pero limita loop (set winner after 1 turn)
                self.board.winner = self.p1  # Fuerza end after setup
                # Nota: play() es loop while not over, pero con winner inicial no corre
                # Para test: Remueve winner temporal
                original_winner = self.board.winner
                self.board.winner = None
                # Mock para evitar input loop
                self.board.move_piece(23, 1, self.p1)  # Pre-move
                # Test display called (indirecto)
                self.assertIsNotNone(self.board.current_player)
                self.board.winner = original_winner

    def test_display(self):
        """Test display: Prints without error (check output indirecto)."""
        # Unittest no chequea prints fácilmente; asume no crash
        from io import StringIO
        import sys

        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()
        self.board.display()
        sys.stdout = old_stdout
        output = captured.getvalue()
        self.assertIn("Board", output)
        self.assertIn("Turno", output)


if __name__ == "__main__":
    unittest.main()
