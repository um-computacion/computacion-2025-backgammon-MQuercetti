from typing import List

from core.board import Board
from core.player import Player


def _candidate_from_points(board: Board, player: Player) -> List[int]:
    """Return candidate from_points considering bar priority and ownership."""
    # Bar priority: if player has checkers on bar, must enter from bar
    if len(board.bar[player]) > 0:
        return [-1] if player.color == "white" else [24]
    # Otherwise, any point with at least one checker belonging to the player
    points = []
    for i in range(24):
        stack = board.points[i]
        if stack and stack[-1].owner == player:
            points.append(i)
    return points


def _valid_from_points_for_die(board: Board, player: Player, die: int) -> List[int]:
    """Filter candidate points to those that produce a valid move for this die."""
    return [
        fp
        for fp in _candidate_from_points(board, player)
        if board.is_valid_move(fp, die, player)
    ]


def _input_from_point(
    prompt: str, valid_choices: List[int], player: Player
) -> int | None:
    """Prompt the user to choose a from_point, allowing 'q' to quit or 'pass' to skip.

    Accepts aliases:
      - 'bar' → -1 for white, 24 for black
    Returns None if user chooses to pass.
    """
    while True:
        raw = input(prompt).strip().lower()
        if raw in {"q", "quit", "exit"}:
            raise KeyboardInterrupt
        if raw in {"p", "pass"}:
            return None
        if raw == "bar":
            choice = -1 if player.color == "white" else 24
        else:
            try:
                choice = int(raw)
            except ValueError:
                print("Invalid input. Enter an integer index, 'bar', or 'pass'.")
                continue
        if choice in valid_choices:
            return choice
        print(f"Invalid point. Valid options: {sorted(valid_choices)} (or 'pass').")


def _play_human_turn(board: Board, player: Player) -> None:
    print(f"\nTurno de {player.name} ({player.color}).")
    dice = board.roll_dice()
    print(f"Dados: {dice}")

    for die in dice:
        valid_froms = _valid_from_points_for_die(board, player, die)
        if not valid_froms:
            print(f"- Sin movimientos válidos para dado {die}.")
            continue
        try:
            fp = _input_from_point(
                prompt=(
                    "Elige punto de origen para mover con dado "
                    f"{die} (valores válidos {sorted(valid_froms)}; 'bar'/'pass'): "
                ),
                valid_choices=valid_froms,
                player=player,
            )
        except KeyboardInterrupt:
            print("\nSaliendo...")
            raise
        if fp is None:
            print("Pasar movimiento.")
            continue
        try:
            board.move_piece(fp, die, player)
            print(f"Movido desde {fp} con {die}.")
        except ValueError as e:
            print(f"Movimiento inválido: {e}")
    board.display()


def _play_ai_turn(board: Board) -> None:
    print("\nTurno de la IA.")
    # La IA actual realiza un movimiento simple sin considerar los dados.
    board.ai.play_turn()
    board.display()


def _choose_mode() -> str:
    print("\nBienvenido a Backgammon!")
    print("Selecciona el modo de juego:")
    print("1. Humano vs IA")
    print("2. Humano vs Humano")
    print("3. Salir")
    while True:
        choice = input("Ingresa 1, 2 o 3: ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("Opción inválida.")


def main() -> None:
    try:
        choice = _choose_mode()
        if choice == "3":
            print("Saliendo. ¡Hasta luego!")
            return

        if choice == "1":
            # Humano vs IA
            name = input("Nombre del jugador humano: ").strip() or "Humano"
            human = Player(name, "white")
            ai_player_entity = Player("Computer", "black")
            board = Board(human, ai_player_entity)
            print("Juego iniciado: Humano (blanco) vs IA (negro).")
            board.display()
            while not board.is_game_over():
                if board.current_player == human:
                    _play_human_turn(board, human)
                else:
                    _play_ai_turn(board)
                if board.is_game_over():
                    break
                board.switch_player()

        elif choice == "2":
            # Humano vs Humano
            name1 = input("Nombre del Jugador 1 (blanco): ").strip() or "Jugador 1"
            name2 = input("Nombre del Jugador 2 (negro): ").strip() or "Jugador 2"
            p1 = Player(name1, "white")
            p2 = Player(name2, "black")
            board = Board(p1, p2)
            print("Juego iniciado: Humano vs Humano.")
            board.display()
            while not board.is_game_over():
                current = board.current_player
                _play_human_turn(board, current)
                if board.is_game_over():
                    break
                board.switch_player()

        winner = board.get_winner() if board.is_game_over() else None
        if winner:
            print(f"\n¡{winner.name} ({winner.color}) gana!")
        else:
            print("\nJuego terminado.")
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")


if __name__ == "__main__":
    main()
