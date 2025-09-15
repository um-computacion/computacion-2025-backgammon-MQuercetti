import unittest
from core.checkers import checkers


class DummyPlayer:
    def __init__(self, name):
        self.name = name


class TestCheckers(unittest.TestCase):
    def test_checker_owner_assignment(self):
        """
        TDD: Verifica que la ficha se asigna correctamente al jugador.
        """
        player = DummyPlayer("Player1")
        checker = checkers(player)
        self.assertEqual(checker.owner, player)

    def test_checker_repr(self):
        """
        TDD: Verifica la representación de la ficha.
        """
        player = DummyPlayer("Player2")
        checker = checkers(player)
        self.assertIn("Player2", repr(checker))


if __name__ == "__main__":
    unittest.main()
