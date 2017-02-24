from cell import *
from sneku import *
from classicSneku import *
from diagonalSneku import *
from random import randint

import json
import logging

logger = logging.getLogger('battlesneku')
hdlr = logging.FileHandler('hssssst.log')
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

class Game:
    def __init__(self, snekNames, height = 17, width = 17, appleMax = 5, appleRate = 5):
        self.snekNames = snekNames
        self.height = height
        self.width = width
        self.apples = [[]]
        self.snekus = []
        self.grid = []
        self.appleMax = appleMax
        self.appleRate = appleRate
        self.tick = 0
        
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
                
            try:
                if self.snekNames[i] == "classic":
                    print "Creating classicSneku"
                    sneku = classicSneku(snakeHouse[0], snakeHouse[1], colours[i], (self.height, self.width))
                elif self.snekNames[i] == "diagonal":
                    print "Creating diagonalSneku"
                    sneku = diagonalSneku(snakeHouse[0], snakeHouse[1], colours[i], (self.height, self.width))
                else:
                    print "ERROR: %s is not a real snek. Go make it! Using the dumb snake instead" % self.snekNames[i]
                    sneku = Sneku(snakeHouse[0], snakeHouse[1], colours[i], (self.height, self.width))
                self.snekus.append(sneku)
            except IndexError:
                print "ERROR: There are not at least %s sneks defined. Go make more! Using the dumb snake instead" % i
                sneku = Sneku(snakeHouse[0], snakeHouse[1], colours[i], (self.height, self.width))
                self.snekus.append(sneku)
                    
        self.apples = [tastyTuna]
        
        print "Start game... apples: %s. snake: %s" % (self.apples, snakeHouse)
        
    def loadState(self, board):
        print board
        self.height = board['height']
        self.width = board['width']
        self.tick = board['tick']
        self.apples = board['apples']
        self.appleMax = board['appleMax']
        self.appleRate = board['appleRate']
        
        for key, value in board['snekus'].iteritems():
            if value["type"] == "classic":
                sneku = classicSneku(value["head"][0], value["head"][1], key, (self.height, self.width))
                sneku.body = value["body"]
                sneku.score = value["score"]
                sneku.life = value["life"]
            elif value["type"] == "diagonal":
                sneku = diagonalSneku(value["head"][0], value["head"][1], key, (self.height, self.width))
                sneku.body = value["body"]
                sneku.score = value["score"]
                sneku.life = value["life"]
            elif value["type"] == "scaredy":
                sneku = scaredySneku(value["head"][0], value["head"][1], key, (self.height, self.width))
                sneku.body = value["body"]
                sneku.score = value["score"]
                sneku.life = value["life"]
                
            self.snekus.append(sneku)
        
        
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
        
    def makeMoves(self):
        board = self.getBoard()
        logger.info(json.dumps(board))
        for sneku in self.snekus:
            if sneku.dead == False:
                m = sneku.makeMove(board)
                newPos = [sneku.head[0] + m[0], sneku.head[1] + m[1]]
                sneku.body.append(newPos)
                #print "(%s): %s" % (sneku.colour, m)
        
    def updateBoard(self):
        for sneku in self.snekus:
            if len(sneku.body) > sneku.length:
                sneku.body = sneku.body[1:]
            sneku.head = sneku.body[-1]
            if sneku.dead == False:
                sneku.life -= 1
                
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
        if randint(0, self.appleRate) == 0 or len(self.apples) == 0:
            if len(self.apples) < self.appleMax:
                self.spawnNewApple()
                
        self.tick += 1
            
    def getBoard(self):
        board = {
            "height": self.height,
            "width": self.width,
            "apples": self.apples,
            "snekus": {},
            "tick": self.tick,
            "appleMax": self.appleMax,
            "appleRate": self.appleRate,
        }
        
        for sneku in self.snekus:
            if sneku.dead == False:
                board['snekus'][sneku.colour] = {
                    "body": sneku.body,
                    "head": sneku.head,
                    "score": sneku.score,
                    "life": sneku.life,
                    "type": sneku.getType(),
                }
            
        return board
                
                
