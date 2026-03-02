class Cell:
    def __init__(self) -> None:
        self.walls = 15
        self.visited = False
        self.blocked = False

    def has_wall(self, direction: int) -> bool:
        return (self.walls & direction) != 0

    def remove_wall(self, direction: int) -> None:
        self.walls &= ~direction

    def __str__(self) -> str:
        return "Cell"
