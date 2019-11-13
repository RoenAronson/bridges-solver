from Node import *
from Problem import *

class board:
    # A board is essentially a state of configuration during the puzzle.
    # For example, the initial state is that we have a board with no connections.
    # If we connect two islands, this creates an entirely different 'board' than
    # the initial state.

    # The board has a grid (which becomes a list of lists) representing the
    # the locations of empty nodes/bridges/islands on the board.
    grid = []

    # It also has a set of unique islands on that board.
    islands = set()

    # The heuristic is the most important aspect of the board. Certain boards are
    # more desirable than others in our search for a solution. The heuristic is
    # is the difference of the total required number of connections (a sum of
    # each individual island's required connections), and the total number of
    # connections already made.
    heuristic = 0
    bridgesConnected = 0
    bridgesToConnect = 0


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