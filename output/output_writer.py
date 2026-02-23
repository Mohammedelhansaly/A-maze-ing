from maze.Maze import Maze
from solving.DFS import DFSGenerator
from solving.BFS import BSFSolver
from validation.maze_validator import mazeValidator
from validation.validate_connectivity import ValidateConnectivity3X3EREA
from pydantic import ValidationError


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
                                 exit_=(19, 14))
    maze = Maze(mazevalidate.width, mazevalidate.height, mazevalidate.entry,
                mazevalidate.exit_)
    dfs = DFSGenerator(maze, seed=42)
    dfs.draw_42()
    dfs.generate()

    for row in maze.grid:
        print([cell.walls for cell in row])
    solver = BSFSolver(maze)
    path = solver.BFS()
    validate = ValidateConnectivity3X3EREA(maze)
    if not validate.is_connected():
        raise ValueError("Maze is not fully connected")
    if not validate.open_erea3X3():
        raise ValueError("Maze contains open 3x3 area")
    # if not validate.is_perfect():
    #     raise ValueError("maze is not perfect")
    writer = MazeWriter(maze, path)
    writer.write_config("maze_output.txt")
except ValidationError as e:
    for error in e.errors():
        print(error['msg'])
except ValueError as e:
    print(e)
