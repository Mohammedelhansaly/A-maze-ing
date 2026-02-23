from collections import deque


class ValidateConnectivity3X3EREA:
    def __init__(self, maze):
        self.maze = maze

    def is_connected(self):
        # sx, sy = self.maze.entry
        queue = deque()
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
            for dx, dy, wall in [(0, -1, 1), (0, 1, 4), (1, 0, 2), (-1, 0, 8)]:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
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
