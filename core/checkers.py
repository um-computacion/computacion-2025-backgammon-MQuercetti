from core.player import Player

class Checkers:
    def __init__(self, owner: Player): self.__owner__ = owner
    def get_owner(self): return self.__owner__
