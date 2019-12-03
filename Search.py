from Board import *
from Problem import problem1, problem2
from Node import *
from Search import switch
import copy

# This is the main search function. When the original boardstate is initialized,
# it imports a pre-defined problem-space, and creates a boardstate from it.
# 
# Then the search begins. The initial board is added to frontier, popped, and 
# then children are generated. These are processed and given a score, where 
# the highest scoring are placed at the top of the frontier. Then the search
# is repeated until a complete boardstate is found.

#==============================================================================#
#======  Fields  ==============================================================#
#==============================================================================#

problem = problem2

currentBoard = 0

frontier = []
visited = []

#=============================================================================#
#=======  Methods  ===========================================================#
#=============================================================================#

# This is the first function called during search. This sets up the intial board
# state as defined by the problem.
def initialize():

    # Make the first board-state, with the appropriate size (and heuristic = 0).
    initialBoard = board(problem.boardSize, 0)

    # Populate the board fields with the islands from the problem.
    initialBoard.fromProblem(problem)

    # Populate the board's possible moves. This is needed for the heuristic calculation.
    initialBoard.generateMoves()

    # Now calculate the heuristic of the initial board
    #   by passing in the number of steps taken so far (0) to the heuristic fxn.
    initialBoard.calculateHeuristic()

    # Append the initialBoard to the frontier
    frontier.append(initialBoard)

#=============================================================================#

def search(runs):

    global currentBoard
    global frontier

    # For each run...
    for i in range(runs):

        print("Run number: ", i)

        # Set the currentboard to the first in the frontier, then remove it.
        # This SHOULD be the board with the best heuristic.
        currentBoard = frontier[0]
        frontier.remove(currentBoard)

        # Check to see if the current board is the solution.
        if currentBoard.isFinished():
            print("Finished with ", i, "steps!")
            printPath(currentBoard)
            break

        else:

            # Place that board on the visited list right away.
            visited.append(currentBoard)

            # Generate children of the current board state.
            makeChildren(currentBoard)

            # Sort the frontier by board state heuristic
            frontier.sort(key=lambda x: x.heuristic)

#==============================================================================#

# Generate a list of children from the current board state.
def makeChildren(board):

    global frontier
    global visited

    toBeAdded = []
    for move in board.moves:

        # This needs to be done since deepcopy DOES NOT behave correctly
        boardCopy = board.copyFromCurrent()

        # Grab the names of the islands in the move.
        nameList = list(move)
        nameA = nameList.pop()
        nameB = nameList.pop()

        # Check to see if these nodes can actually be connected.
        if board.checkFullConnection(nameA, nameB):
            continue

        # Finally, connect them. 
        # However, if this results in an illegal board state, then penalize.
        # If connection COMPLETES the puzzle, give it a good score.
        penalty = boardCopy.connect(nameA, nameB) 

        # If this is contained within visited, or frontier, do not append.
        if containsBoard(visited, boardCopy):
            input('visited contains')
            continue
        if containsBoard(frontier, boardCopy):
            input('frontier contains')
            continue

        # Now generate the copy's moves and heuristic
        boardCopy.generateMoves()
        boardCopy.calculateHeuristic()
        boardCopy.heuristic += penalty

        # Add to the list of states that will be added to the frontier.
        toBeAdded.append(boardCopy)
                
    # Add new states, then remove duplicates.

    frontier = frontier + toBeAdded
    frontier = cleanFrontier(frontier)

#==============================================================================#

# Take a list of islands, copy each island to a list, and then return the list.
# def copyNodes(boardCopy):

#     islandList = []
#     for island in boardCopy.islands:

#         # Make a new node, with all important information
#         a = copy.copy(island)
#         boardCopy.grid[island.location[0]][island.location[1]] = a
#         islandList.append(a)
    
#     return islandList

#==============================================================================#

# Check to see if the frontier or visited list contain a board
def containsBoard(boardList, boardCopy):

    for board in boardList:
        if boardCopy.getBridgeString() == board.getBridgeString():
            return True
    return False

#==============================================================================#


# Remove duplicates from frontier. DEBUG ONLY. 
def cleanFrontier(frontier):

    indicesToRemove = []
    for i in range(0, len(frontier)):
        firstBoard = frontier[i]
        for j in range(i+1, len(frontier)):
            nextBoard = frontier[j]
            if firstBoard.getBridgeString() == nextBoard.getBridgeString():
                indicesToRemove.append(j)

    indicesToRemove = set(indicesToRemove)
    indicesToRemove = list(indicesToRemove)

    for index in sorted(indicesToRemove, reverse=True):
        del frontier[index]

    return frontier


#===========================================================================================#

# Prints a viewable boardstate
def printSolution(board):
    for y in range(problem.boardSize):
        toBePrinted = ''
        for x in range(problem.boardSize):
            toBe = board.grid[x][y]
            if toBe == 1:
                printChar = 'o'
            elif toBe == 2:
                printChar = '0'
            elif toBe == 'I':
                location = [x,y]
                name = board.getNameByLocation(location)
                weight = board.islandMap.get(name).get('weight')
                printChar = str(weight)
            else:
                printChar = ' '
            toBePrinted = toBePrinted + printChar + ' '
        print(toBePrinted)

#=======================================================================#

def printBoards(boardList):
    for board in boardList:
        board.printSolution()
        print("=============================")

#==================================================================#

def printPath(board):
    input("hit enter to print board path")
    print("=============")
    board.printSolution()

    nextParent = board.parent
    while nextParent != None:
        print("================")
        nextParent.printSolution()
        nextParent = nextParent.parent

#==============================================================================#

def QWE():
    for board in frontier:
        print(board.heuristic)

def ASD():
    print("##=== Printing frontier boards ===###")
    for i in range(len(frontier)-1, -1, -1):
        board = frontier[i]
        print(board.heuristic)
        print("----")
        board.printSolution()
        print("==================")
    print("##=== end === ##")

def ZXC():
    print("##=== Printing visited boards ===###")
    for board in visited:
        print(board.heuristic)
        print("----")
        board.printSolution()
        print("==================")
    print("##=== end === ##")

#==============================================================================#
#======  Running the Search  ==================================================#
#==============================================================================#

initialize()
search(0)


    


