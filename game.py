from cell import *
from sneku import *
import random

class Game:
    def __init__(self):
        self.life = 100
        self.score = 0
        self.height = 5
        self.width = 5
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
        ax = random.randint(0,self.height - 1)
        ay = random.randint(0,self.width - 1)
        self.apple = [ax, ay]
        sx = random.randint(0,self.height - 1)
        sy = random.randint(0,self.width - 1)
        sneku = Sneku(sx, sy, (self.height, self.width), self.apple)
        self.snekus.append(sneku)
        
    def resetGame(self):
        self.life = 100
        self.score = 0
        self.apple = []
        self.snake = []