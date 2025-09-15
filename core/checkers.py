class Checkers:
    def __init__(self, owner):
        self.owner = owner

    def __repr__(self):
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