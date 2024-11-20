#!/usr/bin/env python
import time
import generator
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
            maze = generator.newMaze(int(xCells), int(yCells))
            dfsolver = solver.MazeSolver(maze, xCells, yCells)
            amogi = dfsolver.solveFindAmogus()
            
            for row in maze:
                for cell in row:
                    if cell.wall:
                        self.matrix.SetPixel(cell.col, cell.row, 0, 40, 30)
                    elif cell.door:
                        self.matrix.SetPixel(cell.col, cell.row, 139,69,19)
                    else:
                        self.matrix.SetPixel(cell.col, cell.row, 0, 0, 5)

            pr = 100
            pg = 20
            pb = 0

            for amog in amogi:
                skip = False
                for cell in amog:
                    if cell.visited:
                        skip = True
                if amog[5].wall or amog[7].wall or amog[3].wall or amog[13].wall or not amog[9].wall:
                    skip = True
                if amog[1].wall == amog[11].wall:
                    skip = True

                if not skip:
                    for cell in amog:
                        if not cell.wall:
                            self.matrix.SetPixel(cell.col, cell.row, pr, pg, pb)
                            self.visual.draw(cell.col, cell.row, (255,0,0))
                        cell.visited = True

            time.sleep(3)


# Main function
if __name__ == "__main__":
    Mazey = Maze()
    if (not Mazey.process()):
        Mazey.print_help()
