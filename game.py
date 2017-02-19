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
        tastyTuna = self.getRandomCoords()
        
        snakeHouse = self.getRandomCoords()
        while snakeHouse == tastyTuna:
            snakeHouse = self.getRandomCoords()
            
        sneku = Sneku(snakeHouse[0], snakeHouse[1], (self.height, self.width), tastyTuna)
        self.snekus.append(sneku)
        self.apple = tastyTuna
        
        #snakeHouse = [0,13]
        #tastyTuna = [15,16]
        #sneku = Sneku(snakeHouse[0], snakeHouse[1], (self.height, self.width), tastyTuna)
        #self.snekus = []
        #self.snekus.append(sneku)
        #self.apple = tastyTuna
        
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
        
        while tastyTuna == self.apple or tastyTuna in self.snekus[0].body:
            tastyTuna = self.getRandomCoords()

        self.apple = tastyTuna
        print "New apple spawned at: %s" % tastyTuna
        
    def updateBoard(self):
        for sneku in self.snekus:
            if sneku.head[0] < 0 or sneku.head[0] >= self.height:
                sneku.killSnake()
            if sneku.head[1] < 0 or sneku.head[1] >= self.width:
                sneku.killSnake()
            
            if sneku.life <= 0:
                sneku.killSnake()
            
            if len([x for x in sneku.body if sneku.body.count(x) > 1]):
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
            board['snekus'].append(sneku.body)
            
        return board
                
                