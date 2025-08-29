from core.player import player
from core.dice import dice

class board:
    def __init__(self, player1: player, player2: player):
        self.player1 = player1
        self.player2 = player2
        self.dice1 = dice()
        self.dice2 = dice()
        self.winner = None
        self.current_player = player1
