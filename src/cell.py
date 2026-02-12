N, E, S, W = 1, 2, 4, 8


class Cell:
    def __init__(self):
        self.walls = N | E | S | W
