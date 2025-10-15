from core.board import Board
from core.player import Player


class Game:
    """
    A class used to represent the overall Backgammon game, coordinating board and players.

    Attributes
    ----------
    __board__ : Board
        The game board.
    __players__ : list of Player
        The list of players.
    __current_player_index__ : int
        Index of the current player.

    Methods
    -------
    start_game()
        Starts the game.
    play_turn()
        Plays a turn for the current player.
    is_game_over()
        Checks if the game is over.
    """

    def __init__(self, player1: Player, player2: Player):
        """
        Constructs all the necessary attributes for the game object.

        Parameters
        ----------
        player1 : Player
            The first player.
        player2 : Player
            The second player.
        """
        self.__board__ = Board(player1, player2)
        self.__players__ = [player1, player2]
        self.__current_player_index__ = 0

    def start_game(self):
        """
        Starts the game.

        Returns
        -------
        None
        """
        print("Game started!")

    def play_turn(self):
        """
        Plays a turn for the current player.

        Returns
        -------
        None
        """
        current_player = self.__players__[self.__current_player_index__]
        dice = self.__board__.roll_dice()
        # Lógica para mover (simplificada)
        self.__board__.switch_player()
        self.__current_player_index__ = (self.__current_player_index__ + 1) % 2

    def is_game_over(self):
        """
        Checks if the game is over.

        Returns
        -------
        bool
            True if the game is over, False otherwise.
        """
        return self.__board__.is_game_over()


# Para correr
if __name__ == "__main__":
    game = Game("Tú", "IA Negra")
    game.play()
