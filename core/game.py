from core.board import Board
from core.player import Player
from ai import AIPlayer  # Tu AI
from typing import Optional

class Game:
    """
    A class used to represent the overall Backgammon game, orchestrating turns.

    Attributes
    ----------
    board : Board
        The game board.
    human_player : Player
        The human player.
    ai_player : AIPlayer
        The AI opponent.

    Methods
    -------
    play()
        Runs the game loop until over.
    get_human_move(board, die)
        Gets a move from human input.
    """

    def __init__(self, human_name: str = "Human", ai_name: str = "AI"):
        """
        Parameters
        ----------
        human_name : str, optional
            Name for human (default "Human").
        ai_name : str, optional
            Name for AI (default "AI").
        """
        self.human_player = Player(human_name, "white")
        self.ai_player = AIPlayer(ai_name, "black")
        self.board = Board(self.human_player, self.ai_player)

    def play(self):
        """
        Runs the main game loop: Alternates turns until game over.

        Returns
        -------
        None

        Examples
        --------
        >>> game = Game()
        >>> game.play()
        # Plays the game
        """
        print("¡Bienvenido a Backgammon! Humano (white) vs AI (black).")
        self.board.display()

        while not self.board.is_game_over():
            current = self.board.current_player
            print(f"\n--- Turno de {current.name} ({current.color}) ---")
            dice = self.board.roll_dice()

            if current == self.human_player:
                # Turno humano simple (input consola)
                sequence = []
                for die in dice[:2]:  # Simplificado, usa primeros 2
                    while True:
                        try:
                            from_point = int(input(f"Mueve desde punto con {die}: "))
                            if self.board.is_valid_move(from_point, die, current):
                                self.board.move_piece(from_point, die, current)
                                sequence.append((from_point, die))
                                print(f"Movido: {from_point} con {die}")
                                break
                            else:
                                print("Movimiento inválido. Intenta de nuevo.")
                        except ValueError:
                            print("Entrada inválida.")
            else:
                # Turno AI
                self.ai_player.play_turn(self.board)

            self.board.switch_player()
            self.board.display()

        winner = self.board.get_winner()
        if winner:
            print(f"¡{winner.name} ({winner.color}) gana!")
        else:
            print("Empate (raro en Backgammon).")

# Para correr
if __name__ == "__main__":
    game = Game("Tú", "IA Negra")
    game.play()
