from core.board import Board
from core.player import Player
from core.dice import Dice


class Game:
    """
    A class used to represent the overall Backgammon game, coordinating board and players.

    Attributes
    ----------
    board : Board
        The game board.
    players : list of Player
        The list of players.
    current_player_index : int
        Index of the current player.
    dice : Dice
        The dice for the game.
    """

    def __init__(self, players: list['Player'], random_positions=False):
        """
        Constructs all the necessary attributes for the game object.

        Parameters
        ----------
        players : list of Player
            The list of players.
        random_positions : bool, optional
            Whether to start with random checker positions, by default False
        """
        self.players = players
        self.board = Board(players[0], players[1], random_positions=random_positions)
        self.current_player_index = 0
        self.dice = Dice()
        self.initial_rolls = [0, 0]
        self.initial_roll_winner = None

    def get_current_player(self):
        """Returns the current player."""
        return self.players[self.current_player_index]

    def switch_player(self):
        """Switches the turn to the other player."""
        self.current_player_index = 1 - self.current_player_index

    def roll_dice(self):
        """Rolls the dice for the current turn."""
        self.dice.roll()
        if self.dice.get_values()[0] == self.dice.get_values()[1]:
            # Doubles, grant four moves
            self.dice.set_values([self.dice.get_values()[0]] * 4)

    def determine_first_player(self):
        """Players roll one die each to determine who goes first."""
        p1_roll = self.dice.roll_one()
        p2_roll = self.dice.roll_one()
        self.initial_rolls = [p1_roll, p2_roll]

        if p1_roll > p2_roll:
            self.initial_roll_winner = self.players[0]
            self.current_player_index = 0
        elif p2_roll > p1_roll:
            self.initial_roll_winner = self.players[1]
            self.current_player_index = 1
        else:
            # Tie, roll again
            self.initial_roll_winner = None
        
        # The first turn's dice are the initial winning rolls
        if self.initial_roll_winner:
            self.dice.set_values([p1_roll, p2_roll])
            
    def _calculate_and_validate_die_for_move(self, from_point: str | int, to_point: str | int, player: 'Player') -> int | None:
        """
        Calculates the die value for a move, handling special cases like bear-off.
        Returns the die value if the move is valid with the current dice, otherwise None.
        """
        if to_point == 'off':
            return self.board.find_die_for_bear_off(from_point, player, self.dice.get_values())

        if from_point == 'bar':
            die = (24 - to_point) if player.get_color() == 'white' else (to_point + 1)
        else:
            die = abs(to_point - from_point)

        return die if die in self.dice.get_values() else None

    def move(self, from_point: str | int, to_point: str | int):
        """
        Moves a piece after validating the move and finding the correct die.
        """
        player = self.get_current_player()
        die = self._calculate_and_validate_die_for_move(from_point, to_point, player)

        if die is None:
            raise ValueError("Invalid move or no available die for this move.")

        self.board.move_piece(from_point, die, player)
        self.dice.remove_value(die)

    def has_possible_moves(self, player: 'Player') -> bool:
        """Check if the current player has any valid moves with the current dice."""
        return self.board.has_any_valid_moves(player, self.dice.get_values())

    def play_ai_turn(self):
        """
        Executes the AI's turn by choosing and performing its moves.
        Note: This method does NOT roll dice or switch the turn. The UI is responsible
        for managing the turn flow (roll -> play -> switch).
        A local import is used to avoid circular dependencies.
        """
        from core.ai import AIPlayer
        player = self.get_current_player()

        if isinstance(player, AIPlayer):
            # The AI determines all its moves for the turn at once
            moves = player.choose_moves(self.board, self.dice.get_values())
            
            for from_point, to_point in moves:
                try:
                    # Each move is executed sequentially
                    self.move(from_point, to_point)
                except (ValueError, IndexError) as e:
                    # This may happen if the AI's logic produces a sequence of moves
                    # that becomes invalid after an earlier move is made.
                    print(f"AI tried an invalid move and has forfeited the rest of its turn: {from_point}->{to_point}. Error: {e}")
                    break # Stop processing further moves

    def is_game_over(self):
        """Checks if the game is over by seeing if any player has borne off all 15 checkers."""
        for player in self.players:
            if self.board.get_off_board_count(player) == 15:
                return True
        return False

    def get_winner(self):
        """Returns the winner of the game."""
        return self.board.get_winner()
