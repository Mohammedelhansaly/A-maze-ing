class Pattern42:
    def __init__(self, maze):
        self.maze = maze
        self.pattern = [
            [1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1],
        ]

    def draw(self):
        x = (self.maze.width // 2 - len(self.pattern[0]) +
             len(self.pattern[0]) // 2)
        y = self.maze.height // 2 - len(self.pattern) + len(self.pattern) // 2
        for i in range(len(self.pattern)):
            for j in range(len(self.pattern[0])):
                cell = self.maze.get_cell(x + j, y + i)
                # cell.walls = pattern[i][j]
                # if cell.walls == 15:
                #     cell.blocked = True
                if self.pattern[i][j] == 1:
                    cell.blocked = True
