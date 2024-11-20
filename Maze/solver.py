from operator import index
import generator
import math
import time
import random

#path rgb
pr = 100
pg = 20
pb = 0

class MazeSolver:
    def __init__(self, maz, colCells, rowCells):
        self.maze = maz

        self.mazeCellLenRow = colCells
        self.mazeCellLenCol = rowCells

        self.firstcellRow = random.randrange(1, (self.mazeCellLenRow * 2) + 1, 2)
        self.firstcellCol = random.randrange(1, (self.mazeCellLenCol * 2) + 1, 2)
        self.lastcellRow = random.randrange(1, (self.mazeCellLenRow * 2) + 1, 2)
        self.lastcellCol = random.randrange(1, (self.mazeCellLenCol * 2) + 1, 2)

    #Breadth first search
    def solveMaze(self):
        activeCells = []
        neighborList = []
        indexList = []
        solution = []
        indexAcc = 0

        #set first cell
        activeCells.append(self.maze[self.firstcellRow][self.firstcellCol])
        indexList.append([0, self.maze[self.firstcellRow][self.firstcellCol].id])


        complete = False 
        while len(activeCells) != 0 and not complete:
            cell = activeCells.pop(0)


            
            cell.visited = True
            if generator.hasNeighbor(cell, self.maze):
                neighborList.clear()
                
                #north
                if self.maze[cell.row - 1][cell.col].wall == False:
                    neighborList.append(self.maze[cell.row - 2][cell.col])
                #south
                if self.maze[cell.row + 1][cell.col].wall == False:
                    neighborList.append(self.maze[cell.row + 2][cell.col])
                #east
                if self.maze[cell.row][cell.col + 1].wall == False:
                    neighborList.append(self.maze[cell.row][cell.col + 2])
                #west
                if self.maze[cell.row][cell.col - 1].wall == False:
                    neighborList.append(self.maze[cell.row][cell.col - 2])

                for c in reversed(range(len(neighborList))):
                    if neighborList[c].visited:
                        del neighborList[c]
                for neighbor in neighborList:
                    if not neighbor.isFound:

                        indexList.append([indexAcc, neighbor.id])

                        rTemp = int((cell.row + neighbor.row) / 2)
                        cTemp = int((cell.col + neighbor.col) / 2)
                        self.maze[rTemp][cTemp].wall = False

                    

                        if neighbor.row == self.lastcellRow and neighbor.col == self.lastcellCol:
                            complete = True
                            neighborList.clear()
                            break
                        else:
                            activeCells.append(neighbor)
                            neighbor.isFound = True
            indexAcc += 1

        # Select 
        currCell = self.maze[len(self.maze) - 1][len(self.maze[0]) - 1]

        # base.matrix.SetPixel(cell.col, cell.row, pr, pg, pb)
        # base.matrix.SetPixel(len(maze)-2, len(maze[0])-2, pr, pg, pb)

        #monkeybrain
        duoList = indexList[-1]
        currIndex = len(indexList) - 1

        maze1D = []
        #create a 1d list of the maze
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                maze1D.append(self.maze[i][j])

        while True:
            duoList = indexList[currIndex]
            currIndex = duoList[0]
            currCell = maze1D[indexList[currIndex][1]]
            solution.append(currCell)

            print(currCell.row)
            print(currCell.col)
            if currCell.row == self.lastcellRow and currCell.col == self.lastcellCol:

                return solution