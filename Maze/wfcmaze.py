#!/usr/bin/env python
import time
import wfcgenerator
import solver
import os
import sys

script_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from rpimatrix.bindings.python.samples.samplebase import SampleBase
class Maze(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Maze, self).__init__(*args, **kwargs)

    def run(self):
        width = self.matrix.width
        height = self.matrix.height
        xCells = max(1, (width/2)-1) #harcoded for 64(should equal 31 for a 64x64 real) pixels
        yCells = max(1, (height/2)-1) #harcoded for 64(should equal 31 for a 64x64 real) pixels

        while True:
            maze = wfcgenerator.newMaze(int(xCells), int(yCells))
            for row in maze:
                for cell in row:
                    if cell.wall:
                        self.matrix.SetPixel(cell.col, cell.row, 0, 40, 30)
                    elif cell.door:
                        self.matrix.SetPixel(cell.col, cell.row, 150, 0, 0)
                    else:
                        self.matrix.SetPixel(cell.col, cell.row, 0, 0, 5)

            solver.solveMaze(maze, self)


            time.sleep(3)


# Main function
if __name__ == "__main__":
    Mazey = Maze()
    if (not Mazey.process()):
        Mazey.print_help()
