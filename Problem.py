from Node import node


class problem:
    # A problem is essentially a collection of islands, their x-y coordinates,
    # and their required number of bridges. It initially has no islands.
    islands = []

    # Since the size of the board depends completely on the size of the problem,
    # we carry that information here. It is initially set to 0.
    boardSize = 0

    # We pass our desired islands and board size into the problem constructor.
    def __init__(self, islands, boardSize):
        self.boardSize = boardSize
        self.islands = islands


# This is just a list of islands we used for our test problem (problem1)
a = node(1, [0, 0], 2)
b = node(1, [0, 3], 4)
c = node(1, [0, 6], 3)
d = node(1, [2, 1], 2)
e = node(1, [2, 3], 6)
f = node(1, [2, 5], 1)
g = node(1, [4, 0], 5)
h = node(1, [4, 3], 5)
i = node(1, [4, 5], 1)
j = node(1, [6, 0], 4)
k = node(1, [6, 2], 2)
l = node(1, [6, 4], 1)
m = node(1, [6, 6], 2)

problem1 = problem([a,b,c,d,e,f,g,h,i,j,k,l,m], 7)

# An alternative test problem.
a2 = node(1, [0, 0], 2)
b2 = node(1, [4, 0], 1)
c2 = node(1, [2, 0], 5)
d2 = node(1, [2, 2], 3)
e2 = node(1, [4, 2], 1)

problem2 = problem([a2,b2,c2,d2,e2], 5)