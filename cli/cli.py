import random
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
        # Chequear si puede retirar
        can_bear_off = _can_bear_off(board, player, die)
        if not valid_froms and not can_bear_off:
            print(f"- Sin movimientos válidos para dado {die}.")
            continue
        
        prompt = (
            "Elige punto de origen para mover con dado "
            f"{die} (valores válidos {sorted(valid_froms)}; 'bar'/'pass'"
        )
        if can_bear_off:
            prompt += "; 'retirar' para bear-off)"
        else:
            prompt += "): "
        
        try:
            choice = input(prompt).strip().lower()
            if choice == "pass":
                print("Pasar movimiento.")
                continue
            elif choice == "retirar" and can_bear_off:
                # Elegir ficha para retirar
                home_points = range(0, 6) if player.color == "white" else range(18, 24)
                bear_off_froms = [p for p in home_points if len(board.points[p]) > 0 and board.is_valid_move(p, die, player)]
                if bear_off_froms:
                    fp = int(input(f"Elige punto para retirar (opciones: {bear_off_froms}): "))
                    if fp in bear_off_froms:
                        board.move_piece(fp, die, player)
                        print(f"Ficha retirada desde {fp} con {die}.")
                        if board.off_board[player] == 15:
                            print(f"¡{player.name} gana!")
                            board.winner = player
                            return
                    else:
                        print("Punto inválido.")
                        continue
                else:
                    print("No hay fichas para retirar con este dado.")
                    continue
            else:
                fp = _parse_from_point(choice, player)
                if fp not in valid_froms:
                    print("Punto inválido.")
                    continue
        except KeyboardInterrupt:
            print("\nSaliendo...")
            raise
        except ValueError:
            print("Entrada inválida.")
            continue
        
        # Guardar off_board antes del movimiento
        off_before = board.off_board[player]
        try:
            board.move_piece(fp, die, player)
            from_display = "bar" if fp in [-1, 24] else fp
            print(f"Movido desde {from_display} con {die}.")
            # Chequear si se retiró una ficha
            if board.off_board[player] > off_before:
                print("¡Ficha retirada del tablero!")
                if board.off_board[player] == 15:
                    print(f"¡{player.name} gana!")
                    board.winner = player
                    return
        except ValueError as e:
            print(f"Movimiento inválido: {e}")
    board.display()

def _can_bear_off(board: Board, player: Player, die: int) -> bool:
    """Chequea si el player puede hacer bear-off con el dado."""
    home_points = range(0, 6) if player.color == "white" else range(18, 24)
    return any(len(board.points[p]) > 0 and board.is_valid_move(p, die, player) for p in home_points)

def _parse_from_point(choice: str, player: Player) -> int:
    """Parsea la entrada del usuario para from_point."""
    if choice == "bar":
        return -1 if player.color == "white" else 24
    return int(choice)

# No olvides importar 'Player' si no lo tienes ya en los encabezados
from core.player import Player

def _play_ai_turn(board: Board, player: Player) -> None:
    print(f"\nTurno de {player.name} ({player.color}).")
    dice = board.roll_dice()
    
    # La lógica ahora está dentro de la clase AIPlayer.
    # Simplemente le pasamos los dados y ella se encarga del resto.
    board.ai.play_turn(dice)
    
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
                    _play_ai_turn(board, ai_player_entity)
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