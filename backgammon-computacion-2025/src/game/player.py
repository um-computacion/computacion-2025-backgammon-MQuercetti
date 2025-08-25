class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.is_active = True

    def deactivate(self):
        self.is_active = False
