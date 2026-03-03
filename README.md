*This project has been created as part of the 42 curriculum by moel-han*
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