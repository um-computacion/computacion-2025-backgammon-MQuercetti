class Checkers:
    """
    A class used to represent a checker piece in the game.

    Attributes
    ----------
    owner : Player
        The player who owns this checker.

    Methods
    -------
    __repr__()
        Returns a string representation of the checker.
    """

    def __init__(self, owner):
        """
        Parameters
        ----------
        owner : Player
            The player who owns this checker.
        """
        self.owner = owner

    def __repr__(self):
        """
        Returns a string representation of the checker.

        Returns
        -------
        str
            A string in the format 'Checkers(owner)'.

        Examples
        --------
        >>> from core.player import Player
        >>> p = Player("Alice")
        >>> c = Checkers(p)
        >>> repr(c)
        'Checkers(player(Alice))'
        """
        return f"Checkers({self.owner})"

    def can_move(self, from_point, to_point, player):
        # Verifica si el movimiento es válido
        if not self.points[from_point]:
            return False
        checker = self.points[from_point][-1]
        if checker.owner != player:
            return False
        # El destino no puede tener más de una ficha del oponente
        destination = self.points[to_point]
        if destination and destination[0].owner != player and len(destination) > 1:
            return False
        return True

    def move_checker(self, from_point, to_point, player):
        if not self.can_move(from_point, to_point, player):
            raise ValueError("Movimiento inválido")
        checker = self.points[from_point].pop()
        destination = self.points[to_point]
        # Captura si hay una sola ficha del oponente
        if destination and destination[0].owner != player and len(destination) == 1:
            captured = destination.pop()
            # Aquí podrías enviar la ficha capturada a la barra
        self.points[to_point].append(checker)
