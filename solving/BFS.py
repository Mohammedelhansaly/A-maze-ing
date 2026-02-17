from collections import deque
from maze.Maze import Maze
from .DFS import DFSGenerator


class BSFSolver:
    def __init__(self, maze):
        self.maze = maze

    def get_accessible_neighbors(self, x, y):
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

    def reconstruct_path(self, parent, start, end):
        path = []
        current = end
        while current != start:
            path.append(current)
            current = parent[current]
        path.append(start)
        path.reverse()
        return path

    def BFS(self):
        start = self.maze.entry
        end = self.maze.exit
        queue = deque([start])
        visited = set()
        visited.add(start)
        parent = {}
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


maze = Maze(10, 20, (0,0),(9,19))
dfs = DFSGenerator(maze)
dfs.generate()
solver = BSFSolver(maze)
path = solver.BFS()
print(path)