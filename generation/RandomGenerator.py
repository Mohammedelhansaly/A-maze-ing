import random
from .DFS import DFSGenerator
from maze.Maze import Maze
from typing import Optional


class RandomGenerator:
    def __init__(self, maze: Maze, seed: Optional[int] = None) -> None:
        self.maze = maze
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def get_unvisted_neignbors(self, x: int, y: int) -> list:
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

    def remove_corner(self, x, y, nx, ny):
        cell = self.maze.get_cell(x, y)
        if cell.has_wall(1) and y > 0:
            self.maze.remove_wall_between(x, y, nx, ny)
        if cell.has_wall(4) and y < self.maze.height - 1:
            self.maze.remove_wall_between(x, y, nx, ny)
        if cell.has_wall(2) and x < self.maze.width - 1:
            self.maze.remove_wall_between(x, y, nx, ny)
        if cell.has_wall(8) and x > 0:
            self.maze.remove_wall_between(x, y, nx, ny)

    def generate(self) -> None:
        dfs = DFSGenerator(self.maze)
        dfs.generate()
        for _ in range((self.maze.width * self.maze.height) // 4):
            x = random.randint(0, self.maze.width - 1)
            y = random.randint(0, self.maze.height - 1)
            direction = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            dx, dy = random.choice(direction)
            nx = x + dx
            ny = y + dy
            # cell = self.maze.get_cell(x, y)
            if (
                0 <= nx < self.maze.width and 0 <= ny < self.maze.height
                and not self.maze.get_cell(nx, ny).blocked
            ):
                self.maze.remove_wall_between(x, y, nx, ny)
                self.remove_corner(x, y, nx, ny)

             
