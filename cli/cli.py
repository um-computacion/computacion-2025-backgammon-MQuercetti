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
    return [fp for fp in _candidate_from_points(board, player) if board.is_valid_move(fp, die, player)]


def _input_from_point(prompt: str, valid_choices: List[int], player: Player) -> int | None:
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

