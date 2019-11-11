from Node import *
from Problem import *

class board:

    # A 'board' represents a state of the game-board.
    # In a typical bridges game, the board initially has no connection. This is
    # the starting state. When the player makes a new connection, the game-board
    # is now in a new state, distinctly different from the previous (in that, it
    # now has ONE connection).

    # We use instances of boards to represents states of the bridges game as out
    # algorithm chooses moves.

    # Each state has a set of islands and those islands
    # have attributes unique to this state (such as connected islands, bridges
    # remaining, etc). The state also has a 'heuristic' measurement of how close
    # it is the goal.

    islands = set()
    heuristic = 0

    # Initializing a board only populates it with empty nodes and gives it a
    # heuristic. Adding the actual islands/connections is done elsewhere.
    def __init__ (self, size, heuristic):
        initGrid = []
        self.heuristic = heuristic
        for i in range(0, size):
            initGrid.append([])
            for j in range(0, size):
                initGrid[i].append(node(-1,[i,j]))
        self.grid = initGrid.copy()

    def printIslands(self):
        for island in islands:
            print(island.location, island.weight - island.connectedBridges )