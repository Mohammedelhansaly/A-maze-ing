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

    def remove_isolated_walls(self):
        for x in range(self.maze.width):
            for y in range(self.maze.height):

                cell = self.maze.get_cell(x, y)

                # check left/right corridor
                if x > 0 and x < self.maze.width - 1:
                    left = self.maze.get_cell(x - 1, y)
                    right = self.maze.get_cell(x + 1, y)

                    if (
                        not left.has_wall(2) and
                        not right.has_wall(8) and
                        cell.has_wall(2) and
                        cell.has_wall(8)
                    ):
                        cell.remove_wall(2)
                        cell.remove_wall(8)

                # check top/bottom corridor
                if y > 0 and y < self.maze.height - 1:
                    top = self.maze.get_cell(x, y - 1)
                    bottom = self.maze.get_cell(x, y + 1)

                    if (
                        not top.has_wall(4) and
                        not bottom.has_wall(1) and
                        cell.has_wall(1) and
                        cell.has_wall(4)
                    ):

                        cell.remove_wall(1)
                        cell.remove_wall(4)

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
        # self.remove_isolated_walls()
