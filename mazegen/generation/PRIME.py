import random
from maze.Maze import Maze
from typing import Optional


class PrimeGenerator:
    DIRECTIONS = [(0, -1), (0, 1), (1, 0), (-1, 0)]

    def __init__(self, maze: Maze, seed: Optional[int] = None) -> None:
        self.maze = maze
        if seed is not None:
            random.seed(seed)

    def get_unvisited_neighbors(self, x: int, y: int) -> list:
        neighbors = []
        for dx, dy in self.DIRECTIONS:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                cell = self.maze.get_cell(nx, ny)
                if not cell.visited and not cell.blocked:
                    neighbors.append((nx, ny))
        return neighbors

    def generate(self) -> None:
        start_x = random.randint(0, self.maze.width - 1)
        start_y = random.randint(0, self.maze.height - 1)

        start_cell = self.maze.get_cell(start_x, start_y)
        start_cell.visited = True

        frontier = self.get_unvisited_neighbors(start_x, start_y)

        while frontier:
            idx = random.randint(0, len(frontier) - 1)
            fx, fy = frontier[idx]
            frontier[idx] = frontier[-1]
            frontier.pop()

            cell = self.maze.get_cell(fx, fy)
            if cell.visited:
                continue

            visited_neighbors = []
            for dx, dy in self.DIRECTIONS:
                nx = fx + dx
                ny = fy + dy
                if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                    neighbor = self.maze.get_cell(nx, ny)
                    if neighbor.visited and not neighbor.blocked:
                        visited_neighbors.append((nx, ny))

            if visited_neighbors:
                vx, vy = random.choice(visited_neighbors)
                self.maze.remove_wall_between(vx, vy, fx, fy)
                cell.visited = True
                for nx, ny in self.get_unvisited_neighbors(fx, fy):
                    if (nx, ny) not in frontier:
                        frontier.append((nx, ny))
