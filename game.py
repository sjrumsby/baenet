from cell import *
from sneku import *
import random

class Game:
    def __init__(self, height = 17, width = 17):
        self.height = height
        self.width = width
        self.apple = []
        self.snekus = []
        self.grid = []
        
        for i in range(self.height):
            row = []
            for j in range(self.width):
                c = Cell(i,j)
                
                for sneku in self.snekus:
                    if [i,j] in sneku.body:
                        c.content = 1
                    
                if [i,j] == self.apple:
                    c.content = -1
                    
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
            
            sneku = Sneku(snakeHouse[0], snakeHouse[1], colours[i], (self.height, self.width), tastyTuna)
            self.snekus.append(sneku)
        self.apple = tastyTuna
        
        print "Start game... apple: %s. snake: %s" % (self.apple, snakeHouse)
        
    def resetGame(self):
        self.life = 100
        self.score = 0
        self.apple = []
        self.snekus = []
        
    def getRandomCoords(self):
        x = random.randint(0,self.height - 1)
        y = random.randint(0,self.width - 1)
        return [x,y]
        
    def spawnNewApple(self):
        tastyTuna = self.getRandomCoords()
        snekuBodies = []
        for sneku in self.snekus:
            for s in sneku.body:
                snekuBodies.append(s)
                
        #Make sure we don't spawn the tuna on s sneku!
        while tastyTuna == self.apple or tastyTuna in snekuBodies:
            tastyTuna = self.getRandomCoords()

        self.apple = tastyTuna
        print "New apple spawned at: %s" % tastyTuna
        
    def updateBoard(self):
        for sneku in self.snekus:
            otherSnekus = [s for s in self.snekus if s != sneku and s.dead == False]
            
            #If we stepped outside the board
            if sneku.head[0] < 0 or sneku.head[0] >= self.height:
                sneku.killSnake()
            if sneku.head[1] < 0 or sneku.head[1] >= self.width:
                sneku.killSnake()
            
            #If our life reaches zero
            if sneku.life <= 0:
                sneku.killSnake()
            
            #If we stepped on ourself
            if len([x for x in sneku.body if sneku.body.count(x) > 1]):
                sneku.killSnake()
        
            #If we stepped onto someone else
            for o in otherSnekus:
                if sneku.head in o.body:
                    sneku.killSnake()
            
            if sneku.head == self.apple:
                self.spawnNewApple()
                sneku.eatApple(self.apple)

                
    def getBoard(self):
        board = {
            "height": self.height,
            "width": self.width,
            "apple": self.apple,
            "snekus": []
        }
        
        for sneku in self.snekus:
            if sneku.dead == False:
                board['snekus'].append(sneku.body)
            
        return board
                
                