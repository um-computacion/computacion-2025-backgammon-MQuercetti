from game.player import player
from game.dice import dice

class Board:
    def __init__(self):
        self.players = []
        self.current_turn = 0
        self.board_state = self.initialize_board()

    def initialize_board(self):
        # Initialize the board state
        return [[None for _ in range(8)] for _ in range(8)]
