from Board import board
from Problem import problem1, problem2
from Node import *
import copy

problem = problem1

currentBoard = 0

frontier = []
visited = []

totalValues = 0

def initialize():
    global currentBoard
    n = problem.boardSize
    initialBoard = board(n, 0, 0)
    for island in problem.islands:
        x = island.location[0]
        y = island.location[1]
        initialBoard.grid[x][y] = island
        initialBoard.islands.add(island)
    currentBoard = copy.deepcopy(initialBoard)
    frontier.append(currentBoard)
    visited.append(currentBoard)

def printIslands(board):
    for island in board.islands:
        print(island.location, island.weight-island.connectedBridges)

def calculateValues(board):
    global totalValues
    for island in board.islands:
        totalValues = totalValues + island.weight


def copyNodes(islands):
    islandList = []
    for island in islands:
        a = node(1, island.location, island.weight, island.connectedBridges)
        a.bridges = island.bridges
        a.connectedIslands = island.connectedIslands
        islandList.append(a)
    return islandList

# Compares all of the bridges in the current board and each board in the frontier. It will only get added to the frontier if it doesn't exist already in the frontier.
def compareBoards(boardCopy, boardList):
    for board in boardList:
        for col in board.grid:
            for cell in col:
                bCell = boardCopy.grid[cell.location[0]][cell.location[1]]
                # If the same node has the same amount of bridges
                if bCell.family != cell.family:
                    return False
                if bCell.bridges != cell.bridges:
                    return False
    return True
                    
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
                if cCell.location == island.location and not checkFullPair(cCell, island):
                    adjacents.append(island)
            break
    for x in range(ax+1,problem.boardSize):
        cCell = board.grid[x][ay]
        if cCell.family == 1 and not cCell.checkFull():
            for island in board.islands:
                if cCell.location == island.location and not checkFullPair(cCell, island):
                    adjacents.append(island)
            break
    for y in range(ay-1,-1,-1):
        cCell = board.grid[ax][y]
        if cCell.family == 1 and not cCell.checkFull():
            for island in board.islands:
                if cCell.location == island.location and not checkFullPair(cCell, island):
                    adjacents.append(island)
            break
    for y in range(ay+1,problem.boardSize):
        cCell = board.grid[ax][y]
        if cCell.family == 1 and not cCell.checkFull():
            for island in board.islands:
                if cCell.location == island.location and not checkFullPair(cCell, island):
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
        print("same column")
        return(checkRow(ax, ay, by, aLoc, bLoc, board))
    # Same Row
    if ay == by:
        print("same row")
        return(checkCol(ay, ax, bx, aLoc, bLoc, board))       

def checkFullPair(nodeA, nodeB):
    a = nodeA
    b = nodeB
    aFull = nodeA.checkFull()
    bFull = nodeB.checkFull()
    return aFull or bFull

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
        nodeA.connectedIslands.append(nodeB.location)
        nodeB.connectedIslands.append(nodeA.location)

def calculateHeuristic(board):
    totalBridges = 0
    for island in board.islands:
        totalBridges = totalBridges + island.connectedBridges
    return (totalValues - totalBridges)

movesTotal = 1
# Generate possible moves given a boardstate
# This means only adjacent nodes that aren't full
def generateMoves(board):
    global movesTotal
    moves = set()
    adj = []
    for island in board.islands:
        adj = (populateAdjacent(island, board))
        print(len(adj))
        for x in adj:
            if not checkFullPair(island, x):
                a = (island,x)
                moves.add((frozenset(a)))
    print("Number of moves:", len(moves))
    movesTotal = len(moves)
    return moves

def makeChildren(board):
    global finished
    for move in (generateMoves(board)):
        boardCopy = copy.deepcopy(board)
        boardCopy.islands = copyNodes(boardCopy.islands)
        mList = list(move)
        a = mList.pop()
        b = mList.pop()
        for island in boardCopy.islands:
            if island.location == a.location:
                a = island
            if island.location ==  b.location:
                b = island
        connect(a, b, boardCopy)
        print(a.location, b.location)
        visited.append(board)
        # Fill fields of new board
        boardCopy.bridgesToConnect = calculateHeuristic(boardCopy)
        boardCopy.bridgesConnected = boardCopy.bridgesConnected + 1
        boardCopy.heuristic = boardCopy.bridgesConnected + boardCopy.bridgesToConnect

        # Add new board to the frontier if it has not already been explored.
        x = compareBoards(boardCopy, visited)
        
        if not x:
            frontier.append(boardCopy)

def checkFinished(board):
    bridges = 0
    weight = 0
    for island in board.islands:
        bridges = bridges + island.connectedBridges
        weight = island.weight + weight
    return bridges == weight



def search(runs):
    global lastBoard
    global currentBoard
    steps = 0
    for i in range(runs):
        if checkFinished(frontier[0]):
            print("Finished with ", i, "steps!")
            break
        else:
            makeChildren(frontier[0])
            lastBoard = frontier.pop(0)
            frontier.sort(key=lambda x: x.heuristic)
            currentBoard = frontier[0]
            printIslands(currentBoard)


initialize()
lastBoard = frontier[0]
finished = False
calculateValues(currentBoard)
currentBoard.heuristic = calculateHeuristic(currentBoard)
search(10000)
# printIslands(currentBoard)


for x in frontier[0].islands:
    for y in frontier[1].islands:
        if x == y:
            print(x.location, y.location)
