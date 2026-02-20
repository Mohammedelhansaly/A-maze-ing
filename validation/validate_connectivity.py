from collections import deque


class ValidateConnectivity3X3EREA:
    def __init__(self, maze):
        self.maze = maze

    def is_connected(self):
        total = self.maze.width * self.maze.height
        sx, sy = self.maze.entry
        queue = deque()
        queue.append((sx, sy))
        visited = set()
        visited.add((sx, sy))

        while queue:
            x, y = queue.popleft()
            cell = self.maze.get_cell(x, y)
            if not cell.has_wall(1):
                nx, ny = x, y - 1
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
            if not cell.has_wall(2):
                nx, ny = x + 1, y
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
            if not cell.has_wall(4):
                nx, ny = x, y + 1
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
            if not cell.has_wall(8):
                nx, ny = x - 1, y
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return len(visited) == total

    def open_erea3X3(self):
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
