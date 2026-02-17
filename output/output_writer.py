class MazeWriter:
    def __init__(self, maze):
        self.maze = maze
        
    def write_path(self):
        
    def write_config(self, filename):
        with open(filename, "w") as filename:
            for row in self.maze.grid:
                line = "".join(hex(cell.walls)[2:] for cell in row)
                filename.write(line + "\n")
            filename.write(f"{self.maze.entry[0]},{self.maze.entry[1]}\n")
            filename.write(f"{self.maze.exit[0]},{self.maze.exit[1]}\n")
            filename.write(f"{self.path}\n")

        