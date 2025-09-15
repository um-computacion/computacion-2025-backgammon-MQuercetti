from core.player import player
from core.dice import dice
from core.checkers import Checkers as checkers


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

    def can_move(self, from_point: int, to_point: int, player):
        if not self.points[from_point]:
            return False
        checker = self.points[from_point][-1]
        if checker.owner != player:
            return False
        destination = self.points[to_point]
        if destination and destination[0].owner != player and len(destination) > 1:
            return False
        return True

    def move_checker(self, from_point: int, to_point: int, player):
        if not self.can_move(from_point, to_point, player):
            raise ValueError("Movimiento inválido")
        checker = self.points[from_point].pop()
        destination = self.points[to_point]
        if destination and destination[0].owner != player and len(destination) == 1:
            captured = destination.pop()
            # Aquí podrías enviar la ficha capturada a la barra
        self.points[to_point].append(checker)
