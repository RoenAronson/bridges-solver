from Node import node


class problem:
    boardSize = 0
    islands = []
    def __init__(self, islands, boardSize):
        self.boardSize = boardSize
        self.islands = islands


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

a2 = node(1, [0, 0], 2)
b2 = node(1, [4, 0], 1)
c2 = node(1, [2, 0], 5)
d2 = node(1, [2, 2], 3)
e2 = node(1, [4, 2], 1)

problem2 = problem([a2,b2,c2,d2,e2], 5)