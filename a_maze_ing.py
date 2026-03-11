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

import curses
from typing import Any, List, Tuple

from drawing.maze_solver import solve_maze
from drawing.maze_draw import (
    draw_maze, draw_menu, apply_theme, rotate_theme, animate_generation
)


def _build_maze(
    config: dict,
) -> Tuple[
    List[List[int]],
    Tuple[int, int],
    Tuple[int, int],
    List[Tuple[int, int, int, int]],
]:
    """
    Generate a maze according to *config*, write the output file, and
    return the display grid, entry/exit positions, and generation steps.

    Args:
        config: validated configuration dictionary.

    Returns:
        grid: 2D list of wall bitmasks ready for drawing.
        entry_pos: (x, y) entry cell.
        exit_pos: (x, y) exit cell.
        steps: ordered list of (x1, y1, x2, y2) wall-removal events that
               produced the maze, suitable for animate_generation().
    """
    mazevalidate = mazeValidator(
        width=config['width'],
        height=config['height'],
        entry=config['entry'],
        exit_=config['exit'],
    )
    maze_obj = Maze(
        mazevalidate.width, mazevalidate.height,
        mazevalidate.entry, mazevalidate.exit_,
    )
    pattern42 = Pattern42(maze_obj)
    pattern42.draw()

    seed = config.get('seed')
    if config['perfect']:
        gen: Any = DFSGenerator(maze_obj, seed=seed)
    else:
        gen = RandomGenerator(maze_obj, seed=seed)
    gen.generate()

    solver = BSFSolver(maze_obj)
    path = solver.BFS()
    validate = ValidateConnectivity3X3EREA(maze_obj)
    if not validate.is_connected():
        raise ValueError("Maze is not fully connected")

    writer = MazeWriter(maze_obj, path or [])
    writer.write_config(config['output_file'])

    grid: List[List[int]] = [
        [cell.walls for cell in row] for row in maze_obj.grid
    ]
    return grid, maze_obj.entry, maze_obj.exit, gen.steps


def parsing(stdscr: Any, config: dict) -> None:
    """
    Main entry point for the Amazing Maze Engine using curses.

    Args:
        stdscr: curses window object.
        config: validated configuration dictionary.
    """
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    apply_theme()

    maze, entry_pos, exit_pos, steps = _build_maze(config)
    solution = solve_maze(maze, entry_pos, exit_pos)

    show_solution = False
    animate_solution = False

    # Animate the initial maze generation cell by cell
    animate_generation(stdscr, steps, len(maze), len(maze[0]),
                       entry_pos, exit_pos)

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

        # Wait for user input
        key = stdscr.getch()

        if key == ord('1'):
            # Re-generate maze and animate the new generation
            maze, entry_pos, exit_pos, steps = _build_maze(config)
            solution = solve_maze(maze, entry_pos, exit_pos)
            show_solution = False
            animate_generation(stdscr, steps, len(maze), len(maze[0]),
                               entry_pos, exit_pos)

        elif key == ord('2'):
            # Toggle solution animation
            show_solution = not show_solution
            animate_solution = show_solution

        elif key == ord('3'):
            # Rotate color theme
            rotate_theme()

        elif key == ord('4'):
            # Quit program
            break


def main() -> None:
    try:
        validate_file = ConfigValidation(sys.argv[1])
        config = validate_file.validate()

        if len(sys.argv) != 2:
            print("Usage: python3 main.py <maze_file.txt>")
            sys.exit(1)

        curses.wrapper(parsing, config)
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
