import random


class DFSGenerator:
    def __init__(self, maze, seed=None) -> None:
        self.maze = maze
        if seed is not None:
            random.seed(seed)

    def generate(self):
        self._dfs(0, 0)

    def get_unvisted_neignbors(self, x, y):
        neighbors = []
        direction = [
            (0, -1),
            (0, 1),
            (1, 0),
            (-1, 0),
        ]
        for dx, dy in direction:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                if not self.maze.get_cell(nx, ny).visited:
                    neighbors.append((nx, ny))
        return neighbors

    def draw_42(self):
        pattern = [
            [1, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1],
        ]
        x = self.maze.width // 2 - len(pattern[0])
        y = self.maze.height // 2 - len(pattern)
        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                cell = self.maze.get_cell(x + j, y + i)
                # cell.walls = pattern[i][j]
                # if cell.walls == 15:
                #     cell.blocked = True
                if pattern[i][j] == 1:
                    cell.blocked = True

    def _dfs(self, x, y):
        cell = self.maze.get_cell(x, y)
        cell.visited = True
        neighbors = self.get_unvisted_neignbors(x, y)
        random.shuffle(neighbors)

        for nx, ny in neighbors:
            neighbor_cell = self.maze.get_cell(nx, ny)
            if not neighbor_cell.visited and not neighbor_cell.blocked:
                self.maze.remove_wall_between(x, y, nx, ny)
                self._dfs(nx, ny)

# maze = Maze(11, 20, (0, 0), (10, 10))
# dfs = DFSGenerator(maze)
# dfs.draw_42()

# dfs.generate()
# for row in maze.grid:
#     print([cell.walls for cell in row])
