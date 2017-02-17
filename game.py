from cell import *
from sneku import *
import random

class Game:
    def __init__(self):
        self.height = 17
        self.width = 17
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
            
    def initGame(self):
        self.apple = self.getRandomCoords()
        
        snakeHouse = self.getRandomCoords()
        while snakeHouse == self.apple:
            snakeHouse = self.getRandomCoords()
            
        sneku = Sneku(snakeHouse[0], snakeHouse[1], (self.height, self.width), self.apple)
        self.snekus.append(sneku)
        
        print "Start game... apple: %s. snake: %s" % (self.apple, snakeHouse)
        
    def resetGame(self):
        self.life = 100
        self.score = 0
        self.apple = []
        self.snake = []
        
    def getRandomCoords(self):
        x = random.randint(0,self.height - 1)
        y = random.randint(0,self.width - 1)
        return [x,y]
        
    def spawnNewApple(self):
        tastyTuna = self.getRandomCoords()
        
        while tastyTuna == self.apple or tastyTuna in self.snekus[0].body:
            tastyTuna = self.getRandomCoords()

        self.apple = tastyTuna
        print "New apple spawned at: %s" % tastyTuna
        
    def updateBoard(self):
        for s in self.snekus:
            if s.head[0] < 0 or s.head[0] >= self.height:
                s.killSnake()
            if s.head[1] < 0 or s.head[1] >= self.width:
                s.killSnake()
        
            if s.head == self.apple:
                self.spawnNewApple()
                s.eatApple(self.apple)

                
                
                
                