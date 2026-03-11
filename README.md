*This project has been created as part of the 42 curriculum by moel-han and sasliman*
<h1 align="center">
  A-maze-ing
<h1>

## Description
A-maze-ing is a python project that generates and solves mazes using classical graph traversal algorithms.
More than just a maze generator, this project is an exploration of algorithmic thinking, clean architecture, and structured software design. Each maze becomes a graph, each cell a node, and each solution a journey from complexity to clarity.
The goal is from random maze generation to shortest-path discovery using BFS and DFS

## Instructions

### Algorithm

#### DFS

The Depth-First Search (DFS) algorithm is a method for traversing or searching tree and graph data structures by exploring as deeply as possible along each branch before backtracking. It uses a stack (or recursion, which implicitly uses a stack) to manage the order of the nodes to be visited.

#### BFS

The Breadth-First Search (BFS) algorithm is a graph traversal method that systematically explores a graph or tree data structure level by level. It starts from a specified source node and visits all its immediate neighbors before moving on to the neighbors of those neighbors

### Compilation

```bash
make install
```
This will install all dependencies listed in requirements.txt and prepare the environment to run the project.

After creating the virtual environment (for example, named `venv`),activate it to start using the project’s dependencies.

```bash
source venv/bin/acivate
```
Before running the project, please ensure that the virtual environment is created and all dependencies are installed and activated.

```bash
make run
```

You can use Python’s built-in debugger
```bash
make debug
```
This will start the program and allow you to step through the code, inspect variables, and find errors.

You can remove temporary files or caches  (e.g., __pycache__, .mypy_cache) to
keep the project environment clean

```bash
make clean
```
To maintain code quality, we use Flake8 for linting and Mypy for type checking.
Execute the following commands before running or committing your project

```bash
make lint
```

## Resources

- [42 A-maze-ing Subject](https://cdn.intra.42.fr/pdf/pdf/200764/en.subject.pdf)
- [DFS algorithm](https://www.geeksforgeeks.org/dsadepth-first-search-or-dfs-for-a-graph/)
- [BFS algorithm](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/)
- [Youtube](https://www.youtube.com/)


////////////////////////////


## Drawing & Animation Module

### Description

The Drawing & Animation module is responsible for the visual representation of the maze in the terminal.

Its purpose is to transform the generated maze data into a clear and interactive ASCII display. This module focuses exclusively on rendering, animation, and user interaction at the display level. It does not implement maze generation or solving algorithms, but instead provides a clean and structured way to visualize them.

By separating the visual layer from the algorithmic logic, the project maintains modularity and clear architectural boundaries.

---

### Features

The module provides the following features:

* Terminal-based ASCII rendering of the maze
* Clear visualization of:

  * Walls
  * Open paths
  * Entry point
  * Exit point
  * Shortest path (when enabled)
* Progressive wall drawing animation
* Smooth screen refresh using the `curses` library
* Clean alignment and structured grid layout
* Ability to show or hide the shortest path
* Re-rendering capability after maze regeneration
* Customizable visual characters (walls, path, entry, exit, solution)

Instead of printing the maze instantly, the renderer progressively draws the structure to create a dynamic construction effect. This improves readability and enhances the user experience.

---

### Usage

After installing dependencies and activating the virtual environment:

```
make run
```

Or run the program directly:

```
python3 main.py maze.txt
```

The renderer will display the maze in the terminal with animated drawing.

Make sure:

* Python 3.10 or later is installed
* Your environment supports the `curses` library (Unix-based systems recommended)
* The maze file is valid and properly generated

---

### Visual Interaction

The terminal interface allows:

* Displaying the generated maze
* Showing or hiding the computed shortest path
* Regenerating and re-rendering a new maze
* Viewing animated wall construction

The animation is handled through controlled frame updates and timed refreshes to ensure smooth rendering without flickering.

---

### Technical Notes

The drawing system:

* Converts maze grid data into a structured terminal canvas
* Maps logical cells to ASCII characters
* Uses screen clearing and controlled refresh cycles
* Ensures consistent alignment regardless of maze dimensions

Special care was taken to handle terminal behavior, screen redraw synchronization, and visual consistency.