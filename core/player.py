class player:
    """Representa un jugador en el juego.

    Attributes:
        name (str): El nombre del jugador.
        color (str): El color de las piezas del jugador.
    """

    def __init__(self, name):
        """
        Inicializa un jugador con un nombre y sin color asignado.

        Args:
            name (str): El nombre del jugador.
        """
        self.name = name
        self.color = None

    def __repr__(self):
        """Devuelve una representación legible del jugador.

        Returns:
            str: Representación en formato 'player(nombre)'.
        """
        return f"player({self.name})"

    def __eq__(self, other):
        """Compara dos jugadores por su nombre.

        Args:
            other (Player): Otro jugador a comparar.

        Returns:
            bool: True si ambos jugadores tienen el mismo nombre, False en caso contrario.
        """
        if isinstance(other, player):
            return self.name == other.name
        return False
