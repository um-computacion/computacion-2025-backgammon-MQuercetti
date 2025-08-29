class dice:
    def __init__(self):
        import random
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        if self.dice1 == self.dice2:
            self.dice1 *= 2
            self.dice2 *= 2
