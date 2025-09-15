class player:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"player({self.name})"

    def __eq__(self, other):
        if isinstance(other, player):
            return self.name == other.name
        return False
