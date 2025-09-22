import unittest
from core.dice import Dice


class TestDice(unittest.TestCase):
    def test_dice_values_are_between_1_and_6(self):
        """
        TDD: Verifica que los valores de los dados estén en el rango válido.
        """
        dice = Dice()
        self.assertTrue(1 <= dice.value1 <= 6)
        self.assertTrue(1 <= dice.value2 <= 6)

    def test_get_moves_returns_two_values_for_regular_roll(self):
        """
        TDD: Verifica que get_moves devuelve dos valores distintos si los dados no son dobles.
        """
        dice = Dice()
        dice.value1 = 2
        dice.value2 = 5
        self.assertEqual(dice.get_moves(), [2, 5])

    def test_get_moves_returns_four_values_for_doubles(self):
        """
        TDD: Verifica que get_moves devuelve cuatro valores iguales si los dados son dobles.
        """
        dice = Dice()
        dice.value1 = 6
        dice.value2 = 6
        self.assertEqual(dice.get_moves(), [6, 6, 6, 6])


if __name__ == "__main__":
    unittest.main()