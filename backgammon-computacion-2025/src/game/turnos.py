from game.player import player
class turnos:


    def __init__(self, player1: player, player2: player):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1

    def switch_turn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1