import random
import sys
from .DFS import DFSGenerator
from maze.Maze import Maze
from typing import Optional

sys.setrecursionlimit(10**6)


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

    def cell_open_neighbor(self, x1: int, y1: int) -> bool:
        cell = self.maze.get_cell(x1, y1)
        direction = [
            (0, -1),
            (0, 1),
            (1, 0),
            (-1, 0),
        ]
        for dx, dy in direction:
            nx = x1 + dx
            ny = y1 + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                neighbor_cell = self.maze.get_cell(nx, ny)
                if neighbor_cell.visited and not cell.blocked and not neighbor_cell.blocked:
                    return True
        return False
    
    def remove_isolated_wall(self, x, y):
        cell = self.maze.get_cell(x, y)

        if not cell.visited:
            return

        neighbors = [
            (x - 1, y),  # left
            (x + 1, y),  # right
            (x, y - 1),  # top
            (x, y + 1)   # bottom
        ]

        for nx, ny in neighbors:
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                neighbor_cell = self.maze.get_cell(nx, ny)
                if self.cell_open_neighbor(x, y):
                    cell.visited = True
                    break

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
            cell = self.maze.get_cell(x, y)
            if (
                0 <= nx < self.maze.width and 0 <= ny < self.maze.height
                and not cell.blocked and not self.maze.get_cell(nx, ny).blocked
            ):
                self.maze.remove_wall_between(x, y, nx, ny)
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                self.remove_isolated_wall(x, y)
