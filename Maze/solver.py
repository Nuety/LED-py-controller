from operator import index
import generator
import math
import time


#path rgb
pr = 100
pg = 20
pb = 0


#Breadth first search
def solveMaze(maze, base):
    activeCells = []
    neighborList = []
    indexList = []
    indexAcc = 0
    colorBias = 0

    #set first cell
    activeCells.append(maze[1][1])
    indexList.append([0, maze[1][1].id])


    complete = False
    while len(activeCells) != 0 and not complete:
        cell = activeCells.pop(0)
        colorBias += 0.001
        if colorBias > 0.3:
            colorBias = 0
        #base.matrix.SetPixel(cell.col, cell.row, 180 - abs(math.sin(colorBias) * 50), 130 + abs(math.sin(colorBias) * 100) , 0)

        cell.visited = True
        if generator.hasNeighbor(cell, maze):
            neighborList.clear()

            #north
            if maze[cell.row - 1][cell.col].wall == False:
                neighborList.append(maze[cell.row - 2][cell.col])
            #south
            if maze[cell.row + 1][cell.col].wall == False:
                neighborList.append(maze[cell.row + 2][cell.col])
            #east
            if maze[cell.row][cell.col + 1].wall == False:
                neighborList.append(maze[cell.row][cell.col + 2])
            #west
            if maze[cell.row][cell.col - 1].wall == False:
                neighborList.append(maze[cell.row][cell.col - 2])

            for c in reversed(range(len(neighborList))):
                if neighborList[c].visited:
                    del neighborList[c]
            for neighbor in neighborList:
                indexList.append([indexAcc, neighbor.id])

                rTemp = int((cell.row + neighbor.row) / 2)
                cTemp = int((cell.col + neighbor.col) / 2)
                maze[rTemp][cTemp].wall = False


                #base.matrix.SetPixel(cell.col, cell.row, 180 , 130 + abs(math.sin(colorBias) * 100) , 0)

                if neighbor.row == len(maze) - 2 and neighbor.col == len(maze[0]) - 2:
                    complete = True
                    neighborList.clear()
                    break
                else:
                    activeCells.append(neighbor)
        indexAcc += 1
    if False:
        for row in maze:
            for cell in row:
                if not cell.wall:
                    base.matrix.SetPixel(cell.col, cell.row, 0, 0, 50)

    currCell = maze[len(maze) - 1][len(maze[0]) - 1]
    prevCell = maze[len(maze) - 1][len(maze[0]) - 1]

    # base.matrix.SetPixel(cell.col, cell.row, pr, pg, pb)
    # base.matrix.SetPixel(len(maze)-2, len(maze[0])-2, pr, pg, pb)

    #monkeybrain
    duoList = indexList[-1]
    currIndex = len(indexList) - 1

    maze1D = []
    #create a 1d list of the maze
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            maze1D.append(maze[i][j])

    while True:
        duoList = indexList[currIndex]
        currIndex = duoList[0]
        currCell = maze1D[indexList[currIndex][1]]

        rTemp = int((currCell.row + prevCell.row) / 2)
        cTemp = int((currCell.col + prevCell.col) / 2)
        base.matrix.SetPixel(cTemp, rTemp, pr, pg, pb)
        time.sleep(0.03)
        base.matrix.SetPixel(currCell.col, currCell.row, pr, pg, pb)
        time.sleep(0.03)




        if currCell.row == 1 and currCell.col == 1:
            base.matrix.SetPixel(1, 1, pr, pg, pb)
            break
        prevCell = currCell