from Node import *
from Problem import *
import copy

switch = False

class board:
    # A board is essentially a state of configuration during the puzzle.
    # For example, the initial state is that we have a board with no connections.
    # If we connect two islands, this creates an entirely different 'board' than
    # the initial state.

#==============================================================================#
#======  Fields  ==============================================================#
#==============================================================================#

    # A board knows about the islands, their names,
    # number of required bridges, and their current connections.
    islandMap = {}

    # A board knows about the state it came from
    parent = None

    # The board has a grid (which becomes a list of lists) representing the
    # the locations of all nodes (empty, bridge, or island).
    ## IT DOES NOT CONTAIN ACTUAL OBJECTS. Instead there are numeric representations
    ## of kind of node.
    grid = []

    # A set moves that are possible from this boardstate
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

#=============================================================================#
#=======  Methods  ===========================================================#
#=============================================================================#

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
                initGrid[i].append(0)
        self.grid = initGrid.copy()

#==============================================================================================#    

# Take a problem space, and populate the board with the problem islands.

    def fromProblem(self, problem):

        self.bridgesRequired = problem.countBridgesRequired() # Get total bridges required
        
        for island in problem.islands: # Copy islands for the problem
            
            # Copy island to appropriate grid location.
            x = island.location[0]
            y = island.location[1]
            self.grid[x][y] = 'I'

            # Open the board's hash map, and look up the entry corresponding to the island's name.
            # Then update it with the required info.
            self.islandMap.update( 
                {
                    island.name: {
                    'location': island.location,
                    'weight': island.weight,
                    'connections': []
                }
                }
                )
        
#==============================================================================================#

# The heuristic is function of the complexity of the board state (number of possible moves)
#   PLUS the number of incomplete islands, 
#   PLUS the number of bridges remaining.
##  NOTE: A-star is not implemented, since it is not applicable to the problem.

    def calculateHeuristic(self):

        self.heuristic = len(self.moves) + (len(self.islandMap) - self.countComplete()) + (self.bridgesRequired - self.bridgesConnected)

        
#================================================================================================#

# Query the dictionary to count the number of incomplete islands.
# This is a function of counting the connections length, and the island weight

    def countComplete(self):
        count = 0
        dic = self.islandMap
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
        for island in self.islandMap:
            count += island.connectedBridges
        return count

#================================================================================================#

    # Look at the board's islandMap. Look up the node by name and see if 
    # its weight is equal to length of connection list. 
    # If equal, return true.
    def checkFullIsland(self, name):
        entry = self.islandMap.get(name)
        if entry.get('weight') == len(entry.get('connections')):
            return True
        else: 
            return False

#================================================================================================#

    # Look at the board's connectedIslands dictionary. Look up the nodes and check to see if 
    # their weights are equal to length of their connection list. 
    # If either are equal, return true.
    def checkFullPair(self, nameA, nameB):

        entryA = self.islandMap.get(nameA)
        if entryA.get('weight') == len(entryA.get('connections')):
            return True

        entryB = self.islandMap.get(nameB)
        if entryB.get('weight') == len(entryB.get('connections')):
            return True

        else:
            return False

#==============================================================================================#

# Look up two islands (by name), and see if they are already connected twice
    def checkFullConnection(self, nameA, nameB):

        # Get A's connection list
        connectionsA = self.islandMap.get(nameA).get('connections')

        # Get the connection entry expected for B
        entryB = [self.getLocationByName(nameB), nameB]

        # Check if entryB appears in the list twice.
        if connectionsA.count(entryB) == 2:
            return True
        else:   
            return False


#================================================================================================#

    def connect(self, nameA, nameB):

    # This will either return a list of nodes to be made into bridges,
    # or it returns false.

        penalty = 0

        toBeBridges = self.checkAdjacent(nameA, nameB)

        if len(toBeBridges) > 0:

            # Actually connecting now...

            # Update the grid first.
            for location in toBeBridges:
                cell = self.gridAtLocation(location)
                if (cell < 2 and cell >= 0):
                    # It must be done this way, selecting indices directly
                    x = location[0]
                    y = location[1]
                    self.grid[x][y] += 1
            
            # Now update the islandMap to reflect what is actually connected.
            self.updateConnected(nameA, nameB)
            self.bridgesConnected = self.bridgesConnected + 1

            # HOWEVER, if the connection completed both islands, we need to see if it's an illegal state.
            if ( self.checkFullIsland(nameA) and self.checkFullIsland(nameB) ):
                penaltyStatus = self.checkIllegalState(nameA)
                if penaltyStatus == True:
                    penalty = 100

        return penalty


        

#=================================================================================================#

    # Update both islands with the connection entry (location of the connected node, and the name)
    def updateConnected(self, nameA, nameB):
        self.islandMap.get(nameA).get('connections').append( list([self.getLocationByName(nameB), nameB]) )
        self.islandMap.get(nameB).get('connections').append( list([self.getLocationByName(nameA), nameA]) )
    


#===================================================================================================#

    # This gets triggered when a connection completes both islands, which can also result in an illegal board state.
    # It could also result in a completed board state, which also check here.
    # This method returns a penalty for the heuristic if the state is illegal.
    def checkIllegalState(self, nameA):

        # Is the board complete?
        if self.isFinished():
            input("we found the complete state")
            return False

        # Initialize an empty list of nodes to be checked, as well as a running sequence of the connected string of nodes.
        toCheck = []
        connectedSequence = []

        # Start with a node from the connection that triggered this event.
        toCheck.append(nameA)

        while len(toCheck) > 0:

            nodeToCheck = toCheck[0] # put first node on the queue
            connections = self.islandMap.get(nodeToCheck).get('connections') # list of node name/location pairs

            # Go through the node's connections, and add them to the queue if they're not already explored.
            for i in range(0, len(connections)):
                connectionName = (connections[i][1])   # A connection = [location, name]. We want the name.
                if connectionName not in connectedSequence:
                    toCheck.append(connectionName)  # add name to the queue

            connectedSequence.append( toCheck.pop(0) ) # add checkedNode to the connections sequence

        # If each island in the connected sequence is full, then it's illegal.
        for name in connectedSequence:
            if not self.checkFullIsland(name):
                return False

        return True

        

        


#====================================================================================================#

    # Find out if the islands are in the same row OR column.
    # Then call the appropriate method to convert nodes to bridges
    def checkAdjacent(self, nameA, nameB):

        aLoc = self.getLocationByName(nameA)
        bLoc = self.getLocationByName(nameB)
        ax = aLoc[0]
        ay = aLoc[1]
        bx = bLoc[0]
        by = bLoc[1]
        print(nameA, self.getLocationByName(nameA))
        print(nameB, self.getLocationByName(nameB))

        # If nodes are in same Column
        if ax == bx:
            return(self.checkColumn(ax, ay, by)) # ax is passed in as the column

        # If nodes are in same row
        if ay == by:
            return(self.checkRow(ay, ax, bx)) # ay is passed in as the row

        else:
            input('coords dont match')

#===========================================================================================#

# checkColumn returns a list of the coordinates to be turned into bridges (that are in the same row).
# In theory, there should not be ANYTHING in the way. We checked for bridges in 'populateAdjacent'

    def checkColumn(self, col, ay, by):
        toBeBridges = []

        # Get the smaller/larger of the two y-coordinates
        smaller = min(ay, by)
        larger = max(ay, by)

        for y in range (smaller+1, larger):
            currCell = self.grid[col][y]
            if currCell == 'I': # If hit an island, then return (SHOULD BE IMPOSSIBLE)
                return False
            toBeBridges.append( [col,y] )
        return toBeBridges

#==============================================================================#

# checkRow does the same thing as checkColumn, except within the same row instead of column.

    def checkRow(self, row, ax, bx):
        toBeBridges = []

        # Get the smaller/larger of the two x-coordinats
        smaller = min(ax, bx)
        larger = max(ax, bx)

        for x in range (smaller+1, larger):
            currCell = self.grid[x][row]
            if currCell == 'I': # If hit an island, then return (SHOULD BE IMPOSSIBLE)
                return False
            toBeBridges.append( [x,row] )
        return toBeBridges

#==============================================================================#

    # Generate all possible moves given a boardstate.
    # A move is defined a pair of island names (which are keys in the island map.)
    def generateMoves(self):

        self.printSolution()

        self.moves = set()

        # For every island that is NOT full (as determined by the hashmap)
        for name in self.islandMap:

            if self.checkFullIsland(name):
                continue

            else:
                # Find all adjacent islands (not blocked by bridges)
                adjacentIslands = self.populateAdjacent(name)

                for adj_name in adjacentIslands:
                    # if the current island and adjacent island still need connections...
                    if not self.checkFullPair(name, adj_name):
                        pair = [name, adj_name]
                        self.moves.add( frozenset(pair) )


#==============================================================================#


    # This will find all islands adjacent to nodeA, regardless if they are blocked by a 
    # bridge. This is accounted for later on...
    def populateAdjacent(self, name):

        islandLocation = self.islandMap.get(name).get('location')
        ax = islandLocation[0]
        ay = islandLocation[1]
        adjacentIslands = []

        # Searching to the left of nodeA...
        for x in range( ax-1,-1,-1 ):

            curr_location = [x, ay]
            curr_value = self.gridAtLocation(curr_location)

            # If you reach an island, and it still needs connections...add to adjacent island list
            if curr_value == 'I':
                if self.checkFullByLocation(curr_location):
                    break
                else:
                    adjacentIslands.append(self.getNameByLocation(curr_location))
                    break

            # If you reach a bridge, then you can go no further.
            # if type(curr_value) == int and curr_value > 0:
            #     break


        # Searching to the right...
        for x in range( ax+1, len(self.grid) ):
            curr_location = [x, ay]
            curr_value = self.gridAtLocation(curr_location)
            if curr_value == 'I':
                if self.checkFullByLocation(curr_location):
                    break
                else:
                    adjacentIslands.append(self.getNameByLocation(curr_location))
                    break


        # Searching above...
        for y in range( ay-1,-1,-1 ):
            curr_location = [ax, y]
            curr_value = self.gridAtLocation(curr_location)
            if curr_value == 'I':
                if self.checkFullByLocation(curr_location):
                    break
                else:
                    adjacentIslands.append(self.getNameByLocation(curr_location))
                    break

        # Searching below...
        for y in range( ay+1, len(self.grid) ):
            curr_location = [ax, y] 
            curr_value = self.gridAtLocation(curr_location)
            if curr_value == 'I':
                if self.checkFullByLocation(curr_location):
                    break
                else:
                    adjacentIslands.append(self.getNameByLocation(curr_location))
                    break


        return adjacentIslands

#==============================================================================#

    def dic(self):
        for entry in self.islandMap:
            print (self.islandMap.get(entry))

#===============================================================================#

    def isFinished(self):
        return self.bridgesConnected == self.bridgesRequired

#==============================================================================#

# Very crude way of creating a board copy. 
# This is used to avoid deepcopying an entire board (which has problems).

    def copyFromCurrent(self):
        newBoard = board(len(self.grid), 0)
        newBoard.islandMap = copy.deepcopy(self.islandMap)
        newBoard.grid = copy.deepcopy(self.grid)
        newBoard.bridgesConnected = copy.deepcopy(self.bridgesConnected)
        newBoard.bridgesRequired = copy.deepcopy(self.bridgesRequired)
        newBoard.stepsSoFar = self.stepsSoFar + 1
        newBoard.heuristic = copy.copy(self.heuristic)
        newBoard.parent = self
        return newBoard

#=================================================================================#

    def printSolution(self):
        for x in range(0, len(self.grid)):
            toBePrinted = ''
            for y in range(0, len(self.grid)):
                cell = self.grid[x][y]
                if cell == 1:
                    printChar = '^'
                elif cell == 2:
                    printChar = '*'
                elif cell == 'I':
                    location = [x, y]
                    name = self.getNameByLocation(location)
                    weight = self.islandMap.get(name).get('weight')
                    printChar = str(weight)
                else:
                    printChar = ' '
                toBePrinted = toBePrinted + printChar + ' '
            print(toBePrinted)


#===============================================================#

# The 'bridgeString' is a unique identifier for the board.
# Basically, turn the grid into a string and return it.

    def getBridgeString(self):
        bridgeString = ''
        for column in self.grid:
            for cell in column:
                bridgeString = bridgeString + str(cell)
        return bridgeString

#===============================================================#

    # Take a name from the hashmap, return node from the grid.print(cell)
    def fromGridByName(self, name):
        entry = self.islandMap.get(name)
        location = entry.get('location')
        x = location[0]
        y = location[1]
        return self.grid[x][y]

#===============================================================#

    def checkFullByLocation(self, location):
        for name in self.islandMap:
            entry = self.islandMap.get(name)
            if entry.get('location') == location:
                return entry.get('weight') == len(entry.get('connections'))

#===============================================================#

    def gridAtLocation(self, location):
        x = location[0]
        y = location[1]
        return self.grid[x][y]

#===============================================================#

    def getNameByLocation(self, location):
        for name in self.islandMap:
            entry = self.islandMap.get(name)
            if entry.get('location') == location:
                return name

#=================================================================#

    def getLocationByName(self, name):
        entry = self.islandMap.get(name)
        return entry.get('location')

