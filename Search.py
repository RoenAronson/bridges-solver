from Board import board
from Problem import problem1
from Node import *
import copy

n = problem1.boardSize

currentBoard = board(n,0,0)

frontier = []

totalValues = 0

def initialize():
    global currentBoard
    initialBoard = board(n, 0, 0)
    for island in problem1.islands:
        x = island.location[0]
        y = island.location[1]
        initialBoard.grid[x][y] = island
        initialBoard.islands.add(island)
    currentBoard = copy.deepcopy(initialBoard)
    frontier.append(currentBoard)

def printIslands(board = currentBoard):
    for island in board.islands:
        print(island.location, island.weight-island.connectedBridges)

def calculateValues(board = currentBoard):
    global totalValues
    for island in board.islands:
        totalValues = totalValues + island.weight
    
# checkRow and Col can return a list of the cells to be turned into bridges.
# This makes it easy to make bridges along the path that we already iterate across.
def checkRow(row, ay, by, aLoc, bLoc, board = currentBoard):
    toBeBridges = []
    if ay < by:
        for i in range(ay+1, by):
            cCell = board.grid[row][i]
            toBeBridges.append(cCell)
            if cCell.family == 1 and cCell.location != bLoc:
                return False
        return toBeBridges
    if ay > by:
        for i in range(by+1, ay):
            cCell = board.grid[row][i]
            toBeBridges.append(cCell)
            if cCell.family == 1 and cCell.location != aLoc:
                return False
        return toBeBridges

def checkCol(col, ax, bx, aLoc, bLoc, board = currentBoard):
    toBeBridges = []
    if ax < bx:
        for i in range(ax+1, bx):
            cCell = board.grid[i][col]
            toBeBridges.append(cCell)
            if cCell.family == 1 and cCell.location != bLoc:
                return False
        return toBeBridges
    if ax > bx:
        for i in range(bx+1, ax):
            cCell = board.grid[i][col]
            toBeBridges.append(cCell)
            if cCell.family == 1 and cCell.location != aLoc:
                return False
        return toBeBridges

def populateAdjacent(nodeA, board = currentBoard):
    ax = nodeA.location[0]
    ay = nodeA.location[1]
    for i in range(0,ax):
        cCell = board.grid[i][ay]
        if cCell.family == 1 and not cCell.checkFull():
            nodeA.adjacentIslands.append(cCell)
    for i in range(ax+1,n):
        cCell = board.grid[i][ay]
        if cCell.family == 1 and not cCell.checkFull():
            nodeA.adjacentIslands.append(cCell)
    for i in range(0,ay):
        cCell = board.grid[ax][i]
        if cCell.family == 1 and not cCell.checkFull():
            nodeA.adjacentIslands.append(cCell)
    for i in range(ay+1,n):
        cCell = board.grid[ax][i]
        if cCell.family == 1 and not cCell.checkFull():
            nodeA.adjacentIslands.append(cCell)


def checkAdjacent(nodeA, nodeB, board = currentBoard):
    aLoc = nodeA.location
    bLoc = nodeB.location
    ax = aLoc[0]
    ay = aLoc[1]
    bx = bLoc[0]
    by = bLoc[1]
    # Same Column
    if ax == bx:
        return(checkRow(ax, ay, by, aLoc, bLoc, board))
    # Same Row
    if ay == by:
        return(checkCol(ay, ax, bx, aLoc, bLoc, board))       

def checkFullPair(nodeA, nodeB):
    a = nodeA
    b = nodeB
    aFull = nodeA.checkFull()
    bFull = nodeB.checkFull()
    return aFull and bFull

fullTest = True

def connect(nodeA, nodeB, board = currentBoard):
    global fullTest
    adjacent = checkAdjacent(nodeA, nodeB, board)
    full = checkFullPair(nodeA, nodeB)
    fullTest = full
    if adjacent and not full:
        # Actually connect
        for cell in adjacent:
            if (cell.bridges < 2 and cell.bridges >= 0) and (cell.family == 0 or cell.family == -1):
                cell.family = 0
                cell.bridges = cell.bridges + 1
        nodeA.connectedBridges = nodeA.connectedBridges + 1
        nodeB.connectedBridges = nodeB.connectedBridges + 1
        nodeA.connectedIslands.append(nodeB)
        nodeB.connectedIslands.append(nodeA)

def calculateHeuristic(board = currentBoard):
    calculateValues(board)
    totalBridges = 0
    for island in board.islands:
        totalBridges = totalBridges + island.connectedBridges
    return totalValues - totalBridges

# Generate possible moves given a boardstate
# This means only adjacent nodes that aren't full
def generateMoves(board = currentBoard):
    moves = set()
    for island in board.islands:
        full = island.checkFull()
        if not full:
            populateAdjacent(island, board)
            for adj in island.adjacentIslands:
                if not adj.checkFull():
                    moves.add(frozenset([island, adj]))
    print("Moves", len(moves))
    return moves

def makeChildren(board = currentBoard):
    for move in (generateMoves(board)):
        boardCopy = copy.deepcopy(board)
        mList = list(move)
        connect(mList.pop(), mList.pop(), boardCopy)
        boardCopy.heuristic = calculateHeuristic(boardCopy)
        frontier.append(board)

def finished(board = currentBoard):
    bridges = 0
    weight = 0
    for island in board.islands:
        bridges = bridges + island.connectedBridges
        weight = island.weight
    return bridges == weight

def search(runs):
    global currentBoard
    for i in range(runs):
        if finished(currentBoard):
            print("Finished!")
            break
        else:
            if (i % 10) == 0:
                print("Still working!")
                print(fullTest)
            makeChildren(currentBoard)
            frontier.sort(key=lambda x: x.heuristic)
            currentBoard = frontier[0]

initialize()
search(10)
printIslands(frontier[0])
print(frontier[0].heuristic)
