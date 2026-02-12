from cell import Cell


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]