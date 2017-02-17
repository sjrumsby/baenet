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
        self.life = 100
        self.score = 0
        self.dead = 0
        
    def makeMove(self):
        if (self.head[0] < self.apple[0]):
            move = self.directions["UP"]
            newPos = [self.head[0] + move[0], self.head[1] + move[1]]
            
            if newPos in self.body:
                move = self.directions["RIGHT"]
                newPos = [self.head[0] + move[0], self.head[1] + move[1]]
        elif (self.head[0] > self.apple[0]):
            move = self.directions["DOWN"]
            newPos = [self.head[0] + move[0], self.head[1] + move[1]]
            
            if newPos in self.body:
                move = self.directions["RIGHT"]
                newPos = [self.head[0] + move[0], self.head[1] + move[1]]
        elif (self.head[1] < self.apple[1]):
            move = self.directions["RIGHT"]
            newPos = [self.head[0] + move[0], self.head[1] + move[1]]
            
            if newPos in self.body:
                move = self.directions["DOWN"]
                newPos = [self.head[0] + move[0], self.head[1] + move[1]]
        elif (self.head[1] > self.apple[1]):
            move = self.directions["LEFT"]
            newPos = [self.head[0] + move[0], self.head[1] + move[1]]
            
            if newPos in self.body:
                move = self.directions["DOWN"]
                newPos = [self.head[0] + move[0], self.head[1] + move[1]]
        else:
            #Arbitrarily go Right when we hit the apple
            move = self.directions["RIGHT"]
        
        self.head[0] += move[0]
        self.head[1] += move[1]
        self.body.append(self.head[:])
        self.life -= 1
        if len(self.body) > self.length:
            self.body = self.body[1:]
        
        print "Moving: %s. Length: %s. Life: %s. Status : %s" % (move, self.length, self.life, self.dead)
        return move
        
    def eatApple(self, apple):
        print apple
        self.length += 2
        self.life = 100
        self.score += 1
        self.apple = apple
        
    def killSnake(self):
        self.dead = 1
