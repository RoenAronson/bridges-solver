from Node import *
from Problem import *

class board:
    grid = []
    islands = set()
    heuristic = 0
    bridgesConnected = 0
    bridgesToConnect = 0
    def __init__ (self, size, iteration, heuristic):
        initGrid = []
        self.heuristic = heuristic
        for i in range(0, size):
            initGrid.append([])
        for i in range(0, size):
            for j in range(0, size):
                initGrid[i].append(node(-1,[i,j]))
        self.grid = initGrid.copy()