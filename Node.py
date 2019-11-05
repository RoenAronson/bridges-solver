
class node:
    # A node is a gridsquare that keeps track of many of the
    # necessary properties of the puzzle
    types = [-1, 0, 1]
    connectedIslands = []
    adjacentIslands = set()
    connectedBridges = 0
    # For islands, weight is the value
    weight = 0
    # For bridges, bridges is the value
    bridges = 0
    typeString = ""
    family = -1
    location = []
    isFull = False
    def __init__ (self, newType, location = [], weight = 0):
        self.location = location
        self.family = newType
        if newType not in self.types:
            print("Type is not valid on", location)
        # Node is an island
        if self.family == 1:
            self.weight = weight
            self.typeString = "island"
        if type == 0:
            self.family = 0
            self.weight = 0
            self.typeString = "bridge"
        if type == -1:
            self.weight = 0
            self.typeString = "empty"



    def checkFull(self):
        # Returns True if full
        return((self.weight - self.connectedBridges) <= 0)