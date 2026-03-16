import sys
from typing import Optional
import random
from collections import deque
from pydantic import BaseModel, Field, model_validator, field_validator

sys.setrecursionlimit(1000000)


class MazeGenerator:
    N, E, S, W = 1, 2, 4, 8
    ALL_WALL = N | E | S | W

    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit_: tuple[int, int]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.grid = [
            [self.Cell() for _ in range(width)]
            for _ in range(height)
        ]

    class Cell:
        def __init__(self) -> None:
            self.walls = 15
            self.visited = False
            self.blocked = False

        def has_wall(self, direction: int) -> bool:
            return (self.walls & direction) != 0

        def remove_wall(self, direction: int) -> None:
            self.walls &= ~direction

        def set_wall(self, walls: int) -> None:
            self.walls = walls

        def __str__(self) -> str:
            return "Cell"

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def remove_wall_between(self, x1: int, y1: int, x2: int, y2: int) -> None:
        cell1 = self.get_cell(x1, y1)
        cell2 = self.get_cell(x2, y2)

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == -1:
            cell1.remove_wall(self.N)
            cell2.remove_wall(self.S)
        elif dx == 0 and dy == 1:
            cell1.remove_wall(self.S)
            cell2.remove_wall(self.N)
        elif dx == 1 and dy == 0:
            cell1.remove_wall(self.E)
            cell2.remove_wall(self.W)
        elif dx == -1 and dy == 0:
            cell1.remove_wall(self.W)
            cell2.remove_wall(self.E)
        else:
            raise ValueError("Cells are not adjacent")

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    class DFSGenerator:
        def __init__(self, maze: 'MazeGenerator',
                     seed: Optional[int] = None) -> None:
            self.maze = maze
            if seed is not None:
                random.seed(seed)

        def generate(self) -> None:
            self._dfs(0, 0)

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

        def _dfs(self, x: int, y: int) -> None:
            cell = self.maze.get_cell(x, y)
            cell.visited = True
            neighbors = self.get_unvisted_neignbors(x, y)
            random.shuffle(neighbors)

            for nx, ny in neighbors:
                neighbor_cell = self.maze.get_cell(nx, ny)
                if not neighbor_cell.visited and not neighbor_cell.blocked:
                    self.maze.remove_wall_between(x, y, nx, ny)
                    self._dfs(nx, ny)

    class Pattern42:
        def __init__(self, maze: 'MazeGenerator') -> None:
            self.maze = maze
            self.pattern = [
                [1, 0, 0, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 0, 1, 1],
                [0, 1, 0, 1, 0],
                [0, 1, 0, 1, 1],
            ]

        def draw(self) -> None:
            x = (self.maze.width // 2 - len(self.pattern[0]) +
                 len(self.pattern[0]) // 2)
            y = (self.maze.height // 2 - len(self.pattern) +
                 len(self.pattern) // 2)
            path42 = []
            for i in range(len(self.pattern)):
                for j in range(len(self.pattern[0])):
                    cell = self.maze.get_cell(x + j, y + i)
                    if self.pattern[i][j] == 1:
                        cell.blocked = True
                        path42.append(((x + i), (y + j)))

                if (self.maze.entry or self.maze.exit) in path42:
                    raise ValueError("Entry/Exit point inside 42 pattern")

    class PrimeGenerator:
        DIRECTIONS = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        def __init__(self, maze: 'MazeGenerator',
                     seed: Optional[int] = None) -> None:
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
                    if (
                        0 <= nx < self.maze.width
                        and 0 <= ny < self.maze.height
                    ):
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

    class RandomGenerator:
        def __init__(self, maze: 'MazeGenerator',
                     seed: Optional[int] = None) -> None:
            self.maze = maze
            self.seed = seed
            if seed is not None:
                random.seed(seed)

        def generate(self) -> None:
            dfs = MazeGenerator.DFSGenerator(self.maze)
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
                    and not cell.blocked
                    and not self.maze.get_cell(nx, ny).blocked
                ):
                    self.maze.remove_wall_between(x, y, nx, ny)

    class BSFSolver:
        def __init__(self, maze: 'MazeGenerator') -> None:
            self.maze = maze

        def get_accessible_neighbors(self, x: int, y: int) -> list:
            neighbors = []
            cell = self.maze.get_cell(x, y)

            if not cell.has_wall(1) and y > 0:
                neighbors.append((x, y - 1))
            if not cell.has_wall(4) and y < self.maze.height - 1:
                neighbors.append((x, y + 1))
            if not cell.has_wall(2) and x < self.maze.width - 1:
                neighbors.append((x + 1, y))
            if not cell.has_wall(8) and x > 0:
                neighbors.append((x - 1, y))
            return neighbors

        def reconstruct_path(self, parent: dict, start: tuple[int, int],
                             end: tuple[int, int]) -> list:
            path = []
            current = end
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path

        def BFS(self) -> Optional[list[tuple[int, int]]]:
            start = self.maze.entry
            end = self.maze.exit
            queue = deque([start])
            visited = set()
            visited.add(start)
            parent: dict[tuple[int, int], tuple[int, int]] = {}
            while (queue):
                x, y = queue.popleft()
                if (x, y) == end:
                    return self.reconstruct_path(parent, start, end)
                for nx, ny in self.get_accessible_neighbors(x, y):
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))
            return None

    class mazeValidator(BaseModel):
        width: int = Field(..., gt=5, lt=100)
        height: int = Field(..., gt=5, lt=100)
        entry: tuple[int, int]
        exit_: tuple[int, int]

        @field_validator("entry", "exit_")
        @classmethod
        def validate_cordinate(cls, v: tuple[int, int]) -> tuple[int, int]:
            x, y = v
            if x < 0 and y < 0:
                raise ValueError("cordinates must be non-negative")
            return v

        @model_validator(mode="after")
        def validate_entry_exit(self) -> "MazeGenerator.mazeValidator":
            if not (0 <= self.entry[0] < self.width and
                    0 <= self.entry[1] < self.height):
                raise ValueError("Entry point is out of maze bounds")
            if not (0 <= self.exit_[0] < self.width and
                    0 <= self.exit_[1] < self.height):
                raise ValueError("Exit point is out of maze bounds")
            if self.entry == self.exit_:
                raise ValueError("Entry and exit points cannot be the same")
            return self

    class ValidateConnectivity3X3EREA:
        def __init__(self, maze: 'MazeGenerator') -> None:
            self.maze = maze

        def is_connected(self) -> bool:
            # sx, sy = self.maze.entry
            queue: deque = deque()
            visited = set()
            start = None
            for y in range(self.maze.height):
                for x in range(self.maze.width):
                    cell = self.maze.get_cell(x, y)
                    if not cell.blocked:
                        start = (x, y)
                        break
                if start:
                    break
            if start is None:
                return False
            queue.append(start)
            visited.add(start)

            while queue:
                x, y = queue.popleft()
                cell = self.maze.get_cell(x, y)
                directions = [(0, -1, 1), (0, 1, 4), (1, 0, 2), (-1, 0, 8)]
                for dx, dy, wall in directions:
                    nx = x + dx
                    ny = y + dy
                    if (
                        0 <= nx < self.maze.width
                        and 0 <= ny < self.maze.height
                    ):
                        neighbor = self.maze.get_cell(nx, ny)
                        if getattr(neighbor, "blocked", False):
                            continue
                        if not (cell.walls & wall):
                            if (nx, ny) not in visited:
                                visited.add((nx, ny))
                                queue.append((nx, ny))
            total = 0
            for y in range(self.maze.height):
                for x in range(self.maze.width):
                    if not getattr(self.maze.get_cell(x, y), "blocked", False):
                        total += 1
            return len(visited) == total

        def open_erea3X3(self) -> bool:
            for y in range(1, self.maze.height - 1):
                for x in range(1, self.maze.width - 1):
                    open_count = 0
                    for dy in range(3):
                        for dx in range(3):
                            cell = self.maze.get_cell(x + dx - 1, y + dy - 1)
                            if cell.walls == 0:
                                open_count += 1
                    if open_count == 9:
                        return False
            return True

    class MazeWriter:
        def __init__(self, maze: 'MazeGenerator', path: list) -> None:
            self.maze = maze
            self.path = path

        def write_path(self) -> str:
            path_str = []
            for i in range(1, len(self.path)):
                px, py = self.path[i - 1]
                x, y = self.path[i]
                dx = x - px
                dy = y - py
                if dx == 1:
                    path_str.append("E")
                elif dx == -1:
                    path_str.append("W")
                elif dy == 1:
                    path_str.append("S")
                elif dy == -1:
                    path_str.append("N")
                else:
                    raise ValueError("invalid path step")
            return "".join(path_str)

        def write_config(self, file: str) -> None:
            with open(file, "w") as filename:
                for row in self.maze.grid:
                    line = "".join(hex(cell.walls)[2:].upper() for cell in row)
                    filename.write(line + "\n")
                filename.write(f"\n{self.maze.entry[0]},"
                               f"{self.maze.entry[1]}\n")
                filename.write(f"{self.maze.exit[0]},{self.maze.exit[1]}\n")
                filename.write(f"{self.write_path()}\n")
