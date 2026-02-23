class Cell:
    def __init__(self):
        self.walls = 15
        self.visited = False
        self.blocked = False

    def has_wall(self, direction):
        return (self.walls & direction) != 0

    def remove_wall(self, direction):
        self.walls &= ~direction

    def __str__(self):
        return "Cell"
