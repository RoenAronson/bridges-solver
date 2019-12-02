from Node import *
from Problem import *
import copy

class board:
    # A board is essentially a state of configuration during the puzzle.
    # For example, the initial state is that we have a board with no connections.
    # If we connect two islands, this creates an entirely different 'board' than
    # the initial state.

    # A board knows which islands are connected to eachother
    connectedIslands = {}

    # A board knows about the state it came from
    parent = None

    # The board has a grid (which becomes a list of lists) representing the
    # the locations of empty nodes/bridges/islands on the board.
    grid = []

    # It also has a set of unique islands on that board.
    islands = []

    # It also has a set moves that are possible from this boardstate
    moves = set()

    # The heuristic is the most important aspect of the board. Certain boards are
    # more desirable than others in our search for a solution. The heuristic is
    # is the sum the remaining number of connections, and the number of steps
    # taken to generate that board.
    # each individual island's required connections), and the total number of
    # connections already made.
    
    bridgesConnected = 0
    stepsSoFar = 0
    bridgesRequired = 0
    heuristic = 0


    # When constructing a board, we need to know the number of columns and rows
    # to create the grid (size), and we need to have some kind of heuristic to
    # associate with it.

    def __init__ (self, size, heuristic):

        # Set the heuristic score
        self.heuristic = heuristic

        # Now make an appropriately sized grid
        initGrid = []
        for i in range(0, size):
            initGrid.append([])
            for j in range(0, size):
                initGrid[i].append(node(-1,[i,j]))
        self.grid = initGrid.copy()

#==============================================================================================#    

# Take a problem space, and populate the board with the required islands.
    def fromProblem(self, problem):
        
        for island in problem.islands: # Copy islands for the problem
            
            # Copy island to appropriate grid location.
            x = island.location[0]
            y = island.location[1]
            self.grid[x][y] = island

        
            self.islands.append(island)
            self.connectedIslands.update( 
                {
                    island.name: {
                    'location': island.location,
                    'weight': island.weight,
                    'connections': []
                }
                }
                )
        
        
        self.bridgesRequired = problem.getTotalWeight() # Get total bridges required


#==============================================================================================#

# Set stepsSoFar and count the number of bridges. 
# Also count the number of incomplete islands, and add that to the total

    def calculateHeuristic(self, steps):

        self.heuristic = (self.bridgesRequired - self.bridgesConnected) + self.stepsSoFar
        
#================================================================================================#

# Query the dictionary to count the number of incomplete islands.
# This is a function of counting the connections length, and the island weight

    def countComplete(self):
        count = 0
        dic = self.connectedIslands
        for key in dic.keys():
            numConnects = len( dic.get(key).get('connections') )
            weight = dic.get(key).get('weight')
            if numConnects == weight:
                count += 1
        return count

#=================================================================================================#

# Counts the number of bridges made so far

    def countBridges(self):
        count = 0
        for island in self.islands:
            count += island.connectedBridges
        return count

#==================================================================================================#

    def getHeuristic(self):
        return self.heuristic

#================================================================================================#

    # Look at the board's connectedIslands dictionary. Look up the nodes and check to see if 
    # their weights are equal to length of their connection list. 
    # If either are equal, return true.
    def checkFullIsland(self, name):
        entry = self.connectedIslands.get(name)
        if entry.get('weight') == len(entry.get('connections')):
            return True

        return False

#================================================================================================#

    # Look at the board's connectedIslands dictionary. Look up the nodes and check to see if 
    # their weights are equal to length of their connection list. 
    # If either are equal, return true.
    def checkFullPair(self, nameA, nameB):
        entry = self.connectedIslands.get(nameA)
        if entry.get('weight') == len(entry.get('connections')):
            return True

        entry = self.connectedIslands.get(nameB)
        if entry.get('weight') == len(entry.get('connections')):
            return True

        return False

#==============================================================================================#

    def checkFullConnection(self, nodeA, nodeB):
        nameA = nodeA.name
        nameB = nodeB.name
        dic = self.connectedIslands
        entry = [nodeB.location, nameB]
        if dic.get(nameA).get('connections').count(entry) == 2:
            return True
        return False


#================================================================================================#

    def connect(self, nodeA, nodeB):

    # This will either return a list of nodes to be made into bridges,
    # or it returns false.

        penalty = 0
        toBeBridges = self.checkAdjacent(nodeA, nodeB)

        full = ( self.checkFullIsland(nodeA.name) or self.checkFullIsland(nodeB.name) )
        if toBeBridges and not full:
            # Actually connect
            for cell in toBeBridges:
                if (cell.bridges < 2 and cell.bridges >= 0):
                    cell.family = 0
                    cell.bridges = cell.bridges + 1
            
            # Now update each island's connected bridges and the board's connected islands
            # nodeA.connectedBridges = nodeA.connectedBridges + 1
            # nodeB.connectedBridges = nodeB.connectedBridges + 1
            self.updateConnected(nodeA, nodeB)
            self.bridgesConnected = self.bridgesConnected + 2

            # However, if the connection completed both islands, we need to see if it's an illegal state.
            if ( self.checkFullIsland(nodeA.name) and self.checkFullIsland(nodeB.name) ):
                penaltyStatus = self.checkIllegalState(nodeA)
                if penaltyStatus == True:
                    penalty = 100
                elif penaltyStatus == 'complete':
                    penalty = -100

        return penalty


        

#=================================================================================================#

    def updateConnected(self, nodeA, nodeB):
        nodeA.connectedBridges += 1
        self.connectedIslands.get(nodeA.name).get('connections').append( list([nodeB.location, nodeB.name]) )
        nodeB.connectedBridges += 1
        self.connectedIslands.get(nodeB.name).get('connections').append( list([nodeA.location, nodeA.name]) )
    


#===================================================================================================#

    def checkIllegalState(self, nodeA):

        if self.isFinished():
            input("we found the complete state")
            return 'complete'


        toCheck = []
        connectedSequence = []

        toCheck.append(nodeA.name)

        while len(toCheck) > 0:

            nodeToCheck = toCheck[0] # put first node on the queue
            connections = self.connectedIslands.get(nodeToCheck).get('connections') # list of node name/location pairs

            for i in range(0, len(connections)):
                connectionName = (connections[i][1])   # 'a' or 'j', etc.
                if connectionName not in connectedSequence:
                    toCheck.append(connectionName)  # add name to the queue

            connectedSequence.append( toCheck.pop(0) ) # add checkedNode to the connections sequence

        if len(connectedSequence) == self.bridgesRequired:
            self.printSolution()
            input("We found a completed board state!")
            return 'complete'

        for name in connectedSequence:
            if not self.checkFullIsland(name):
                return False

        return True

        

        


#====================================================================================================#

    def checkAdjacent(self, nodeA, nodeB):

        aLoc = nodeA.location
        bLoc = nodeB.location
        ax = aLoc[0]
        ay = aLoc[1]
        bx = bLoc[0]
        by = bLoc[1]

        # Now look between the islands to see if there are any islands IN THE WAY.
        # If so, we cannot connect them.

        # If nodes are in same Column
        if ax == bx:
            return(self.checkRow(ax, ay, by, aLoc, bLoc))

        # If nodes are in same row
        if ay == by:
            return(self.checkCol(ay, ax, bx, aLoc, bLoc))

#===========================================================================================#

# checkRow and Col can return a list of the cells to be turned into bridges.
# This makes it easy to make bridges along the path that we already iterate across.
    def checkRow(self, row, ay, by, aLoc, bLoc):
        toBeBridges = []

        if ay < by:
            for i in range(ay+1, by):
                cCell = self.grid[row][i]
                if cCell.family == 1:
                    return False
                toBeBridges.append(cCell)
            return toBeBridges

        if ay > by:
            for i in range(by+1, ay):
                cCell = self.grid[row][i]
                if cCell.family == 1:
                    return False
                toBeBridges.append(cCell)
            return toBeBridges

#==============================================================================#

    def checkCol(self, col, ax, bx, aLoc, bLoc):
        toBeBridges = []

        if ax < bx:
            for i in range(ax+1, bx):
                cCell = self.grid[i][col]
                if cCell.family == 1:
                    return False
                toBeBridges.append(cCell)
            return toBeBridges

        if ax > bx:
            for i in range(bx+1, ax):
                cCell = self.grid[i][col]
                if cCell.family == 1:
                    return False
                toBeBridges.append(cCell)
            return toBeBridges

#==============================================================================#

    # Generate all possible moves given a boardstate
    # This means only adjacent nodes that aren't full
    def generateMoves(self):

        adjacentIslands = []
        self.moves = set()

        for curr_island in self.islands:
            if not self.checkFullIsland(curr_island.name):

                # Find all adjacent islands (regardless if blocked by bridge)
                adjacentIslands = self.populateAdjacent(curr_island)

                for adj_island in adjacentIslands:
                    # if the current island and adjacent island still need connections...
                    if not self.checkFullPair(curr_island.name, adj_island.name):
                        pair = [curr_island, adj_island]
                        self.moves.add( frozenset(pair) )


#==============================================================================#

    # This will find all islands adjacent to nodeA, regardless if they are blocked by a 
    # bridge. This is accounted for later on during...
    def populateAdjacent(self, nodeA):

        ax = nodeA.location[0]
        ay = nodeA.location[1]
        adjacentIslands = []

        # Searching the left of nodeA...
        for x in range( ax-1,-1,-1 ):
            curr_cell = self.grid[x][ay]

            # If you reach an island, and it still needs connections...
            if curr_cell.family == 1 and not curr_cell.checkFull():

                # Check which island it is on the board's island list...
                for island in self.islands:
                    if curr_cell.location == island.location and not self.checkFullPair(curr_cell.name, island.name):
                        # Add that island to the current island  
                        adjacentIslands.append(island)
                break


        # Searching to the right...
        for x in range( ax+1, len(self.grid) ):
            curr_cell = self.grid[x][ay]

            if curr_cell.family == 1 and not curr_cell.checkFull():

                for island in self.islands:
                    if curr_cell.location == island.location and not self.checkFullPair(curr_cell.name, island.name):
                        adjacentIslands.append(island)
                break


        # Searching above...
        for y in range( ay-1,-1,-1 ):
            curr_cell = self.grid[ax][y]

            if curr_cell.family == 1 and not curr_cell.checkFull():

                for island in self.islands:
                    if curr_cell.location == island.location and not self.checkFullPair(curr_cell.name, island.name):
                        adjacentIslands.append(island)
                break

        # Searching below...
        for y in range( ay+1, len(self.grid) ):
            curr_cell = self.grid[ax][y]

            if curr_cell.family == 1 and not curr_cell.checkFull():

                for island in self.islands:
                    if curr_cell.location == island.location and not self.checkFullPair(curr_cell.name, island.name):
                        adjacentIslands.append(island)
                break


        return adjacentIslands

#==============================================================================#

    def dic(self):
        for entry in self.connectedIslands:
            print (self.connectedIslands.get(entry))

#===============================================================================#

    def isFinished(self):
        return self.bridgesConnected == self.bridgesRequired

#==============================================================================#

    def copyFromCurrent(self):
        newBoard = board(len(self.grid), 0)
        newBoard.connectedIslands = copy.deepcopy(self.connectedIslands)
        newBoard.grid = copy.deepcopy(self.grid)
        newBoard.islands = copy.deepcopy(self.islands)
        newBoard.bridgesConnected = copy.deepcopy(self.bridgesConnected)
        newBoard.bridgesRequired = copy.deepcopy(self.bridgesRequired)
        newBoard.stepsSoFar = self.stepsSoFar + 1
        newBoard.heuristic = copy.copy(self.heuristic)
        newBoard.parent = self
        return newBoard

#=================================================================================#

    def printSolution(self):
        for column in self.grid:
            toBePrinted = ''
            for cell in column:
                if cell.bridges == 1:
                    printChar = '^'
                elif cell.bridges == 2:
                    printChar = '*'
                elif cell.family == 1:
                    printChar = str(cell.weight)
                else:
                    printChar = ' '
                toBePrinted = toBePrinted + printChar + ' '
            print(toBePrinted)


#===============================================================#

    def getBridgeString(self):
        bridgeString = ''
        for column in self.grid:
            for cell in column:
                bridgeString = bridgeString + str(cell.bridges)
        return bridgeString
