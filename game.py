from cell import *
from sneku import *
from random import randint

class Game:
    def __init__(self, height = 17, width = 17):
        self.height = height
        self.width = width
        self.apples = [[]]
        self.snekus = []
        self.grid = []
        
        for i in range(self.height):
            row = []
            for j in range(self.width):
                c = Cell(i,j)
                row.append(c)
            self.grid.append(row)
            
    def initGame(self, colours, numSnakes):
        tastyTuna = self.getRandomCoords()
        self.colours = colours
        snakePos = []
        
        for i in range(numSnakes):
        
            snakeHouse = self.getRandomCoords()
            while snakeHouse == tastyTuna or snakeHouse in snakePos:
                snakeHouse = self.getRandomCoords()
            
            sneku = Sneku(snakeHouse[0], snakeHouse[1], colours[i], (self.height, self.width))
            self.snekus.append(sneku)
        self.apples = [tastyTuna]
        
        print "Start game... apples: %s. snake: %s" % (self.apples, snakeHouse)
        
    def resetGame(self):
        self.life = 100
        self.score = 0
        self.apples = [[]]
        self.snekus = []
        
    def getRandomCoords(self):
        x = randint(0,self.height - 1)
        y = randint(0,self.width - 1)
        return [x,y]
        
    def spawnNewApple(self):
        tastyTuna = self.getRandomCoords()
        snekuBodies = []
        for sneku in self.snekus:
            if sneku.dead == False:
                for s in sneku.body:
                    snekuBodies.append(s)
                
        #Make sure we don't spawn the tuna on s sneku!
        while tastyTuna in self.apples or tastyTuna in snekuBodies:
            tastyTuna = self.getRandomCoords()

        self.apples.append(tastyTuna)
        print "New apple spawned at: %s" % tastyTuna
        
    def updateBoard(self):
        sneksToKill = []
        aliveSnekus =  [s for s in self.snekus if s.dead == False]
        
        for sneku in aliveSnekus:
            otherSnekus = [s for s in aliveSnekus if s != sneku and s.dead == False]
            
            #If we stepped outside the board
            if sneku.head[0] < 0 or sneku.head[0] >= self.height:
                print "(%s) SNEK DOWN... Stepped outside the board" % sneku.colour
                sneksToKill.append(sneku)
            if sneku.head[1] < 0 or sneku.head[1] >= self.width:
                print "(%s) SNEK DOWN... Stepped outside the board" % sneku.colour
                sneksToKill.append(sneku)
            
            #If our life reaches zero
            if sneku.life <= 0:
                print "(%s) SNEK DOWN... Died of hunger" % sneku.colour
                sneksToKill.append(sneku)
            
            #If we stepped on ourself
            if len([x for x in sneku.body if sneku.body.count(x) > 1]):
                print "(%s) SNEK DOWN... Ran into itself" % sneku.colour
                sneksToKill.append(sneku)
        
            #If we stepped onto someone else
            for o in otherSnekus:
                if sneku.head in o.body:
                    if sneku.head == o.head:
                        if len(sneku.body) <= len(o.body):
                            print "(%s) SNEK DOWN... Ran into the head of other sneku (%s) and is smaller or equal size" % (sneku.colour, o.colour)
                            sneksToKill.append(sneku)
                    else:
                        print "(%s) SNEK DOWN... Ran into the body of other sneku (%s)" % (sneku.colour, o.colour)
                        sneksToKill.append(sneku)
            
            # Check to see if the snek is getting any apple
            for apple in self.apples: 
                if sneku.head == apple:
                    self.apples.remove(sneku.head)
                    sneku.eatApple()
       
        for soonToBeDeadSneku in sneksToKill:
            soonToBeDeadSneku.killSneku()

        # Spawn new apples at random, or if at 0 apples
        if randint(0,5) == 0 or len(self.apples) == 0:
            if len(self.apples) < 5:
                self.spawnNewApple()
            
    def getBoard(self):
        board = {
            "height": self.height,
            "width": self.width,
            "apples": self.apples,
            "snekus": []
        }
        
        for sneku in self.snekus:
            if sneku.dead == False:
                board['snekus'].append(sneku.body)
            
        return board
                
                