class Sneku:
    directions = {
        "UP": [1, 0],
        "DOWN": [-1, 0],
        "LEFT": [0, -1],
        "RIGHT": [0, 1]
    }
    
    def __init__(self, x, y, dimensions, apple):
        self.head = [x,y]
        self.body = [[x,y]]
        self.dimensions = dimensions
        self.apple = apple
        self.length = 1
        
    def makeMove(self):
        if (self.head[0] < self.apple[0]):
            move = self.directions["UP"]
        elif (self.head[0] > self.apple[0]):
            move = self.directions["DOWN"]
        elif (self.head[1] < self.apple[1]):
            move = self.directions["RIGHT"]
        elif (self.head[1] < self.apple[1]):
            move = self.directions["LEFT"]
        else:
            #Arbitrarily go Right when we hit the apple
            move = self.directions["RIGHT"]
        
        self.head[0] += move[0]
        self.head[1] += move[1]
        self.body.append(self.head)
        
        while len(self.body) > self.length:
            self.body = self.body[1:]
        
        return move
        
    def increaseLength(self):
        self.length += 2