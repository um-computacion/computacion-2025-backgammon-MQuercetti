from player import player
from dice import dice
from checkers import checkers


class Board:
    def __init__(self, player1: player, player2: player):
        self.player1 = player1
        self.player2 = player2
        self.dice1 = dice()
        self.dice2 = dice()
        self.winner = None
        self.current_player = player1
        self.points = self._create_points()

    def _create_points(self):
        # Backgammon tiene 24 puntos, cada uno puede tener fichas de un jugador
        points = [None] * 24
        # Inicialización estándar de backgammon
        # Cada punto es una lista de fichas (checkers)
        points[0] = [checkers(self.player2)] * 2
        points[11] = [checkers(self.player2)] * 5
        points[16] = [checkers(self.player2)] * 3
        points[18] = [checkers(self.player2)] * 5

        points[23] = [checkers(self.player1)] * 2
        points[12] = [checkers(self.player1)] * 5
        points[7] = [checkers(self.player1)] * 3
        points[5] = [checkers(self.player1)] * 5
        # Los demás puntos están vacíos
        for i in range(24):
            if points[i] is None:
                points[i] = []
        return points

    def get_point(self, index: int):
        if 0 <= index < 24:
            return self.points[index]
        raise IndexError("Invalid point index")

    def move_checker(self, from_point: int, to_point: int):
        # Lógica para mover una ficha de un punto a otro
        if not self.points[from_point]:
            raise ValueError("No checker to move")
        checker = self.points[from_point].pop()
        self.points[to_point].append(checker)
