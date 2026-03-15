from typing import List, Tuple


def read_maze_file(
    filename: str
) -> Tuple[
    List[List[int]],
    Tuple[int, int],
    Tuple[int, int],
]:
    """
    Read a maze file and return the maze grid, entry, and exit positions.
    Raises ValueError if the maze is malformed.
    """
    maze: List[List[int]] = []

    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f]

    # Find empty line separating grid and metadata
    try:
        empty_index = lines.index('')
    except ValueError:
        raise ValueError("Maze file missing empty line separator")

    grid_lines = lines[:empty_index]
    metadata_lines = lines[empty_index + 1:]

    if len(metadata_lines) < 2:
        raise ValueError("Maze file missing entry/exit lines")

    # Parse grid
    for line in grid_lines:
        row = [int(c, 16) for c in line]
        maze.append(row)

    # Ensure all rows have same length
    row_lengths = [len(row) for row in maze]
    if min(row_lengths) != max(row_lengths):
        raise ValueError("Malformed maze: inconsistent row lengths")

    # Parse entry/exit
    entry_parts = metadata_lines[0].split(',')
    exit_parts = metadata_lines[1].split(',')
    if len(entry_parts) != 2 or len(exit_parts) != 2:
        raise ValueError("Entry/exit must have 2 coordinates")

    entry_pos: Tuple[int, int] = (int(entry_parts[0]), int(entry_parts[1]))
    exit_pos: Tuple[int, int] = (int(exit_parts[0]), int(exit_parts[1]))

    return maze, entry_pos, exit_pos
