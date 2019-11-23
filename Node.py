
class node:
    # A node is a gridsquare that keeps track of many of the
    # necessary properties of the puzzle.

    # It has a set of x,y coordinates describing it's location on the board
    location = []

    # The node can either be empty (-1), a bridge (0), or an island (1).
    # Nodes are intially empty, with no connected bridges or islands.
    family = -1
    typeString = "empty"
    connectedIslands = []
    connectedBridges = 0

    # IF the node becomes an island, 'weight' is the number of bridges
    # required to complete the island. Empty and bridge nodes have weight = 0.
    weight = 0

    # This is the number of bridges in the node (only if the node is a bridge)
    bridges = 0

    def __init__ (self, newType, location = [], weight = 0, connectedBridges = 0):
        self.location = location
        self.family = newType
        self.connectedBridges = connectedBridges

        if newType not in [-1, 0, 1]:
            print("Type is not valid on", location)

        # During initialization, we do certain things depending on if the node is
        # empty, a bridge, or an island.

        # If it is empty.. we do nothing. The fields are set assuming it is empty.

        # If the node is a bridge...
        if type == 0:
            self.family = 0
            self.typeString = "bridge"

        # If node is an island, set the weight
        if self.family == 1:
            self.weight = weight
            self.typeString = "island"

    # It is useful to know when an island has all it's required bridges.
    def checkFull(self):
        # Returns True if full
        return((self.weight - self.connectedBridges) <= 0)

    def printConnected(self):
        print("Current island: ", self.location)
        for island in self.connectedIslands:
            print(island, " loc")

