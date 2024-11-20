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
            dfsolver = solver.MazeSolver(maze, xCells, yCells)
            solution = dfsolver.solveMaze()
            
            for row in maze:
                for cell in row:
                    if cell.wall:
                        self.matrix.SetPixel(cell.col, cell.row, 0, 40, 30)
                    else:
                        self.matrix.SetPixel(cell.col, cell.row, 0, 0, 5)
            # Draw start and finish
            self.matrix.SetPixel(solution[-1].col, solution[-1].row, 0, 150, 0)

            pr = 100
            pg = 20
            pb = 0
            prevCell = solution[0]
            for currCell in solution:
                # find pixel between two cells
                rTemp = int((currCell.row + prevCell.row) / 2)
                cTemp = int((currCell.col + prevCell.col) / 2)
                # color in temp and current cell
                self.matrix.SetPixel(cTemp, rTemp, pr, pg, pb)
                time.sleep(0.03)
                self.matrix.SetPixel(currCell.col, currCell.row, pr, pg, pb)
                time.sleep(0.03)
                prevCell = currCell

            time.sleep(3)


# Main function
if __name__ == "__main__":
    Mazey = Maze()
    if (not Mazey.process()):
        Mazey.print_help()
