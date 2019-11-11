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

def printIslands(board):
    for island in board.islands:
        print(island.location, island.weight-island.connectedBridges)

def calculateValues(board):
    global totalValues
    for island in board.islands:
        totalValues = totalValues + island.weight

# checkRow and Col can return a list of the cells to be turned into bridges.
# This makes it easy to make bridges along the path that we already iterate across.
def checkRow(row, ay, by, aLoc, bLoc, board):
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

def checkCol(col, ax, bx, aLoc, bLoc, board):
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

def populateAdjacent(nodeA, board):
    ax = nodeA.location[0]
    ay = nodeA.location[1]
    adjacents = []
    for x in range(ax-1,-1,-1):
        cCell = board.grid[x][ay]
        if cCell.family == 1 and not cCell.checkFull():
            for island in board.islands:
                if cCell.location == island.location:
                    adjacents.append(island)
            break
    for x in range(ax+1,n):
        cCell = board.grid[x][ay]
        if cCell.family == 1 and not cCell.checkFull():
            for island in board.islands:
                if cCell.location == island.location:
                    adjacents.append(island)
            break
    for y in range(ay-1,-1,-1):
        cCell = board.grid[ax][y]
        if cCell.family == 1 and not cCell.checkFull():
            for island in board.islands:
                if cCell.location == island.location:
                    adjacents.append(island)
            break
    for y in range(ay+1,n):
        cCell = board.grid[ax][y]
        if cCell.family == 1 and not cCell.checkFull():
            for island in board.islands:
                if cCell.location == island.location:
                    adjacents.append(island)
            break
    return adjacents
        

def checkAdjacent(nodeA, nodeB, board):
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

def connect(nodeA, nodeB, board):
    toBeBridges = checkAdjacent(nodeA, nodeB, board)
    full = checkFullPair(nodeA, nodeB)
    if toBeBridges and not full:
        # Actually connect
        for cell in toBeBridges:
            if (cell.bridges < 2 and cell.bridges >= 0) and not cell.family == 1:
                cell.family = 0
                cell.bridges = cell.bridges + 1
        nodeA.connectedBridges = nodeA.connectedBridges + 1
        nodeB.connectedBridges = nodeB.connectedBridges + 1
        nodeA.connectedIslands.add(nodeB)
        nodeB.connectedIslands.add(nodeA)

def calculateHeuristic(board):
    totalBridges = 0
    for island in board.islands:
        totalBridges = totalBridges + island.connectedBridges
    return totalValues - totalBridges

# Generate possible moves given a boardstate
# This means only adjacent nodes that aren't full
def generateMoves(board):
    moves = set()
    adj = []
    for island in board.islands:
        adj = (populateAdjacent(island, board))
        print(len(adj))
        for x in adj:
            print(checkFullPair(island, x))
            if not checkFullPair(island, x):
                a = (island,x)
                moves.add((frozenset(a)))
    print("Number of moves:", len(moves))
    return moves

def makeChildren(board):
    for move in (generateMoves(board)):
        boardCopy = copy.deepcopy(board)
        mList = list(move)
        print(mList)
        a = mList.pop()
        b = mList.pop()
        for island in boardCopy.islands:
            if island.location == a.location:
                a = island
            if island.location ==  b.location:
                b = island
        connect(a, b, boardCopy)
        boardCopy.heuristic = calculateHeuristic(boardCopy)
        frontier.append(boardCopy)

def finished(board):
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
            makeChildren(currentBoard)
            frontier.sort(key=lambda x: x.heuristic)
            currentBoard = frontier[0]

initialize()
calculateValues(frontier[0])
# frontier[0].heuristic = calculateHeuristic(frontier[0])
# printIslands(frontier[0])
search(1)
# print(len(frontier[0].islands.pop().connectedIslands))
# printIslands(frontier[0])

for x in frontier[0].islands:
    for y in frontier[1].islands:
        if x == y:
            print(x.location, y.location)
