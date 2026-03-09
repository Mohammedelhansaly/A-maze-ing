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

    def cell_open_neighbor(self, x: int, y: int) -> bool:
        directions = [
            (0, -1),
            (0, 1),
            (1, 0),
            (-1, 0),
        ]

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                neighbor = self.maze.get_cell(nx, ny)

                # neighbor is open
                if not neighbor.blocked and neighbor.walls != 15:
                    return True

        return False

    def remove_isolated_wall(self, x: int, y: int):
        cell = self.maze.get_cell(x, y)

        # Only check closed cells
        if cell.walls != 15:
            return

        directions = [
            (0, -1),
            (0, 1),
            (1, 0),
            (-1, 0),
        ]

        open_neighbors = 0

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                neighbor = self.maze.get_cell(nx, ny)

                # neighbor is open
                if neighbor.visited and not neighbor.blocked and neighbor.walls != 15:
                    open_neighbors += 1

        # if all neighbors are open → open this cell
        if open_neighbors == 4:
            cell.set_wall(0)
            cell.visited = True

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
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                self.remove_isolated_wall(x, y)
