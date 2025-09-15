import unittest
from core.player import player


class TestPlayer(unittest.TestCase):
    def test_player_name_assignment(self):
        """
        TDD: Verifica que el nombre del jugador se asigna correctamente.
        """
        p = player("Player1")
        self.assertEqual(p.name, "Player1")

    def test_player_repr(self):
        """
        TDD: Verifica la representación del jugador.
        """
        p = player("Player2")
        self.assertIn("Player2", repr(p))

    def test_player_equality(self):
        """
        TDD: Verifica que dos jugadores con el mismo nombre sean iguales si está implementado __eq__.
        """
        p1 = player("PlayerX")
        p2 = player("PlayerX")
        self.assertEqual(p1, p2)


if __name__ == "__main__":
    unittest.main()
