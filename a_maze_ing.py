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
from generation.PRIME import PrimeGenerator


import curses
from typing import Any

from drawing.maze_io import read_maze_file
from drawing.maze_solver import solve_maze
from drawing.maze_draw import draw_maze, draw_menu, apply_theme, rotate_theme


def parsing(stdscr: Any, filename: str) -> None:
    """
    Main entry point for the Amazing Maze Engine using curses.

    Args:
        stdscr: curses window object.
        filename: path to the maze file to load.
    """
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    apply_theme()

    maze, entry_pos, exit_pos = read_maze_file(filename)

    solution = solve_maze(maze, entry_pos, exit_pos)

    show_solution = False
    animate_solution = False

    # Initial maze build animation
    draw_maze(stdscr, maze, entry_pos, exit_pos, animate_maze=True)

    while True:
        # Draw maze with or without solution
        draw_maze(
            stdscr,
            maze,
            entry_pos,
            exit_pos,
            solution if show_solution else None,
            animate_solution=animate_solution,
        )
        draw_menu(stdscr, len(maze))

        # Reset animation flag after first run
        animate_solution = False
        change_algo = True
        # Wait for user input
        key = stdscr.getch()
        validate_file = ConfigValidation(sys.argv[1])
        config = validate_file.validate()
        maze1 = Maze(config['width'], config['height'],
                     config['entry'],
                     config['exit'])
        pattern42 = Pattern42(maze1)
        pattern42.draw()
        if key == ord('1'):
            # Re-generate maze
            if config['perfect']:
                dfs = DFSGenerator(maze1, seed=config.get('seed'))
                dfs.generate()
            else:
                randomgenerator = RandomGenerator(maze1,
                                                  seed=config.get('seed'))
                randomgenerator.generate()
            write = MazeWriter(maze1, [])
            write.write_config(config['output_file'])
            maze, entry_pos, exit_pos = read_maze_file(config['output_file'])
            solution = solve_maze(maze, entry_pos, exit_pos)
            draw_maze(stdscr, maze, entry_pos, exit_pos, animate_maze=True)

        elif key == ord('2'):
            # Toggle solution animation
            show_solution = not show_solution
            animate_solution = show_solution

        elif key == ord('3'):
            # Rotate color theme
            rotate_theme()

        elif key == ord('4'):
            if change_algo:
                dfs = DFSGenerator(maze1, seed=config.get('seed'))
                dfs.generate()
                change_algo = False
            else:
                prime = PrimeGenerator(maze1, seed=config.get('seed'))
                prime.generate()
                change_algo = True
            write = MazeWriter(maze1, [])
            write.write_config(config['output_file'])
            maze, entry_pos, exit_pos = read_maze_file(config['output_file'])
            solution = solve_maze(maze, entry_pos, exit_pos)
            draw_maze(stdscr, maze, entry_pos, exit_pos, animate_maze=True)
        elif key == ord('5'):
            break


def main() -> None:
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
        # if not validate.open_erea3X3():
        #     raise ValueError("Maze contains open 3x3 area")
        # if not validate.is_perfect():
        #     raise ValueError("maze is not perfect")
        writer = MazeWriter(maze, path or [])
        writer.write_config(config['output_file'])
        if len(sys.argv) != 2:
            print("Usage: python3 main.py <maze_file.txt>")
            sys.exit(1)

        maze, entry_pos, exit_pos = read_maze_file(config['output_file'])
        if maze is None:
            print("Malformed maze detected. Exiting.")
            sys.exit(1)

        curses.wrapper(parsing, config['output_file'])
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
