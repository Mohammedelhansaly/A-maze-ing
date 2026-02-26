import random
from .DFS import DFSGenerator


class RandomGenerator:
    def __init__(self, maze, seed=None):
        self.maze = maze
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def generate(self):
        dfs = DFSGenerator(self.maze)
        dfs.generate()
        for _ in range((self.maze.width * self.maze.height) // 4):
            x = random.randint(0, self.maze.width - 1)
            y = random.randint(0, self.maze.height - 1)
            direction = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            dx, dy = random.choice(direction)
            nx = x + dx
            ny = y + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                self.maze.remove_wall_between(x, y, nx, ny)
