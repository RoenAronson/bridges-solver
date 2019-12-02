from Node import node


class problem:
    # A problem is essentially a collection of islands, their x-y coordinates,
    # and their required number of bridges.

#==============================================================================#
#======  Fields  ==============================================================#
#==============================================================================#

    # The problem contains a list of islands (of the 'node' class)
    islands = []

    # Since the size of the board depends completely on the size of the problem,
    # we carry that information here. It is initially set to 0.
    boardSize = 0

#=============================================================================#
#=======  Methods  ===========================================================#
#=============================================================================#

    # We pass our desired islands and board size into the problem constructor.
    def __init__(self, islands, boardSize):
        self.boardSize = boardSize
        self.islands = islands

    # Count up the number of bridges required.
    # 
    def countBridgesRequired(self):
        bridgesRequired = 0
        for island in self.islands:
            bridgesRequired += island.weight
        return brdigesRequired/2

#=============================================================================#
#=======  Instances  =========================================================#
#=============================================================================#


# This is just a list of islands we used for our test problem (problem1)
a = node(1, [0, 0], 2, name='a')
b = node(1, [0, 3], 4, name='b') 
c = node(1, [0, 6], 3, name='c')
d = node(1, [2, 1], 2, name='d')
e = node(1, [2, 3], 6, name='e')
f = node(1, [2, 5], 1, name='f')
g = node(1, [4, 0], 5, name='g')
h = node(1, [4, 3], 5, name='h')
i = node(1, [4, 5], 1, name='i')
j = node(1, [6, 0], 4, name='j')
k = node(1, [6, 2], 2, name='k')
l = node(1, [6, 4], 1, name='l')
m = node(1, [6, 6], 2, name='m')

problem1 = problem([a,b,c,d,e,f,g,h,i,j,k,l,m], 7)

# An alternative test problem.
a2 = node(1, [0, 0], 2, name='a')
b2 = node(1, [4, 0], 1, name='b')
c2 = node(1, [2, 0], 5, name='c')
d2 = node(1, [2, 2], 3, name='d')
e2 = node(1, [4, 2], 1, name='e')

problem2 = problem([a2,b2,c2,d2,e2], 5)