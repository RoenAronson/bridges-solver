
class node:
    # A node is a gridsquare that keeps track of many of the
    # necessary properties of the puzzle

    # A node can either be empty, a bridge, or an island.
    # The "family" is the variable that indicates
    # the type. Nodes are empty by default, but when constructed, the 'newType'
    # arg determines the node's 'family' (ex: newType = -1 sets family = -1,
    # and typesString = "empty").

    typeString = ""
    family = -1

    # If a node is an island, it will have a list of other islands that are
    # adjacent to it, but not yet connected. A node also has a list of islands
    # that are currently connected to it, as well as a count of it's own total
    # connections. (NOTE: If any island is connected TWICE, then it will be in
    # the connected islands list TWICE).

    adjacentIslands = set()
    connectedIslands = []
    connectedBridges = 0

    # For islands, weight is the value
    weight = 0
    # For bridges, bridges is the value
    bridges = 0
    location = []  # Column, row of the node
    isFull = False  #

    def __init__ (self, newType, location = [], weight = 0):

        # First, check to make sure the type is valid.
        if newType not in [-1, 0, 1]:
            print("Type is not valid on", location)
            return

        # If valid, set the 'type' of node
        self.family = newType

        # Node is an island
        if self.family == 1:
            self.weight = weight
            self.typeString = "island"

        # Node is a bridge
        elif type == 0:
            self.family = 0
            self.weight = 0
            self.typeString = "bridge"

        # Node is empty (neither island nor bridge)
        elif type == -1:
            self.weight = 0
            self.typeString = "empty"

        # Finally, set the location and finish constructing.
        self.location = location



    def checkFull(self):
        # Returns True if full
        return((self.weight - self.connectedBridges) <= 0)