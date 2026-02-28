import sys
from config_validation.config_validation import ConfigValidation
from maze.Maze import Maze
from validation.maze_validator import mazeValidator
from generation.DFS import DFSGenerator
from solving.BFS import BSFSolver
from validation.validate_connectivity import ValidateConnectivity3X3EREA
from output.output_writer import MazeWriter
from pydantic import ValidationError
from generation.RandomGenerator import RandomGenerator
from generation.Pattern42 import Pattern42


def main():
    try:
        validate_file = ConfigValidation(sys.argv[1])
        config = validate_file.validate()
        mazevalidate = mazeValidator(width=config['width'],
                                     height=config['height'],
                                     entry=config['entry'],
                                     exit_=config['exit'])
        maze = Maze(mazevalidate.width, mazevalidate.height,
                    mazevalidate.entry,
                    mazevalidate.exit_)
        pattern42 = Pattern42(maze)
        pattern42.draw()
        if config['perfect']:
            dfs = DFSGenerator(maze, seed=config.get('seed'))
            dfs.generate()
        else:
            randomgenerator = RandomGenerator(maze, seed=config.get('seed'))
            randomgenerator.generate()
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
        writer.write_config(config['output_file'])
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
