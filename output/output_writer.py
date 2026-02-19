from maze.Maze import Maze
from solving.DFS import DFSGenerator
from solving.BFS import BSFSolver
from validation.maze_validator import mazeValidator


class MazeWriter:
    def __init__(self, maze, path):
        self.maze = maze
        self.path = path

    def write_path(self):
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

    def write_config(self, filename):
        with open(filename, "w") as filename:
            for row in self.maze.grid:
                line = "".join(hex(cell.walls)[2:].upper() for cell in row)
                filename.write(line + "\n")
            filename.write(f"\n{self.maze.entry[0]},{self.maze.entry[1]}\n")
            filename.write(f"{self.maze.exit[0]},{self.maze.exit[1]}\n")
            filename.write(f"{self.write_path()}\n")


try:
    mazevalidate = mazeValidator(width=25, height=20, entry=(1, 1),
                                 exit_=(9, 19))
    maze = Maze(mazevalidate.width, mazevalidate.height, mazevalidate.entry,
                mazevalidate.exit_)
    dfs = DFSGenerator(maze, seed=42)
    dfs.generate()
    solver = BSFSolver(maze)
    path = solver.BFS()
    writer = MazeWriter(maze, path)
    writer.write_config("maze_output.txt")
except ValueError as e:
    for error in e.errors():
        print(error['msg'])
