import unittest
from core.player import player
from core.board import Board
from core.dice import dice
from core.checkers import checkers

class DummyPlayer:
    def __init__(self, name):
        self.name = name

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.player1 = DummyPlayer("Player1")
        self.player2 = DummyPlayer("Player2")
        self.board = Board(self.player1, self.player2)

    def test_initial_points_setup(self):
        # TDD: Verifica la cantidad inicial de fichas en los puntos clave
        self.assertEqual(len(self.board.points[0]), 2)
        self.assertEqual(len(self.board.points[11]), 5)
        self.assertEqual(len(self.board.points[16]), 3)
        self.assertEqual(len(self.board.points[18]), 5)
        self.assertEqual(len(self.board.points[23]), 2)
        self.assertEqual(len(self.board.points[12]), 5)
        self.assertEqual(len(self.board.points[7]), 3)
        self.assertEqual(len(self.board.points[5]), 5)

    def test_get_point_valid_and_invalid(self):
        # TDD: Verifica acceso válido e inválido a los puntos
        self.assertIsInstance(self.board.get_point(0), list)
        with self.assertRaises(IndexError):
            self.board.get_point(24)

    def test_can_move_false_no_checker(self):
        # TDD: No se puede mover si no hay ficha en el punto origen
        self.assertFalse(self.board.can_move(3, 4, self.player1))

    def test_can_move_false_wrong_owner(self):
        # TDD: No se puede mover ficha si no pertenece al jugador
        self.assertFalse(self.board.can_move(0, 1, self.player1))  # En 0 están las del player2

    def test_can_move_true(self):
        # TDD: Movimiento válido si hay ficha y destino libre
        self.board.points[4].append(self.board.points[23].pop())
        self.assertTrue(self.board.can_move(4, 6, self.player1))

    def test_move_checker_valid(self):
        # TDD: Movimiento válido mueve la ficha
        self.board.points[4].append(self.board.points[23].pop())
        before = len(self.board.points[4])
        self.board.move_checker(4, 6, self.player1)
        self.assertEqual(len(self.board.points[4]), before - 1)
        self.assertEqual(len(self.board.points[6]), 1)

    def test_move_checker_invalid_raises(self):
        # TDD: Movimiento inválido lanza excepción
        with self.assertRaises(ValueError):
            self.board.move_checker(3, 4, self.player1)

if __name__ == "__main__":
    unittest.main()