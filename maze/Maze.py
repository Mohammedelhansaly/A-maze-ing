from .Cell import Cell
from .Wall import N, E, S, W


class Maze:
    def __init__(self, width, height, entry, exit_):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.grid = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

    def get_cell(self, x, y):
        return self.grid[y][x]

    def remove_wall_between(self, x1, y1, x2, y2):
        cell1 = self.get_cell(x1, y1)
        cell2 = self.get_cell(x2, y2)

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == -1:
            cell1.remove_wall(N)
            cell2.remove_wall(S)
        elif dx == 0 and dy == 1:
            cell1.remove_wall(S)
            cell2.remove_wall(N)
        elif dx == 1 and dy == 0:
            cell1.remove_wall(E)
            cell2.remove_wall(W)
        elif dx == -1 and dy == 0:
            cell1.remove_wall(W)
            cell2.remove_wall(E)
        else:
            raise ValueError("Cells are not adjacent")

    def __str__(self):
        result = ""
        for row in self.grid:
            for cell in row:
                result += f" {cell.wall:2} "
            result += "\n"
        return result
