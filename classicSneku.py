from numpy import array as numpyArray
from heapq import *
from sneku import Sneku

class classicSneku(Sneku):
    def getType(self):
        return "classic"
    
    def makeMove(self, board):
        self.body = board["snekus"][self.colour]["body"]
        self.head = self.body[-1]
        apple = self.getClosestApple(board)
        grid = []
        
        for row in range(board['height']):
            gridRow = []
            for col in range(board['width']):
                g = 0
                for colour, sneku in board['snekus'].iteritems():
                    for snekuBody in board['snekus'][colour]["body"]:
                        if [row, col] == snekuBody:
                            g = 1
                            
                gridRow.append(g)
            grid.append(gridRow)
        
        tuna = tuple(apple)
        head = tuple(self.head)
        tail = tuple(self.body[0])
        
        tunaGrid = list(grid)
        tunaGrid[tail[0]][tail[1]] = 0
        
        nmap = numpyArray(grid)
        tunaMap = numpyArray(tunaGrid)
        
        #ATTACK!
        #This bit will try to eat another snekus head
        for colour, sneku in board['snekus'].iteritems():
            if colour == self.colour:
                continue
            
            if self.manhattanDistance(self.head, sneku['head']) == 2:
                if len(self.body) > len(sneku['body']):
                    print "We should try to eat it's head!"
                    
        #This bit will try to run a snake into the wall
        if len(self.body) > 5:
            #Top wall
            if self.body[-1][0] == 1 and self.body[-2][0] == 1 and self.body[-3][0] == 1:
                for colour, sneku in board['snekus'].iteritems():
                    if colour == self.colour:
                        continue
                        
                    if sneku['head'][0] == 0:
                        if abs(sneku['head'][1] - self.head[1]) >= 2:
                            tmpHead = [sneku['head'][0] + 1, sneku['head'][1]]
                            if tmpHead in self.body:
                                #Okay, now we know we can kill the other sneku. Will we die if we do?
                                newHead = (0, self.head[1])
                                headToTuna = self.astar(nmap, newHead, tuna)
                                
                                if headToTuna:
                                    self.lastMove = [-1, 0]
                                    return [-1, 0]
            
            #Bottom wall
            if self.body[-1][0] == board['height'] - 2 and self.body[-2][0] == board['height'] - 2 and self.body[-3][0] == board['height'] - 2:
                for colour, sneku in board['snekus'].iteritems():
                    if colour == self.colour:
                        continue
                        
                    if sneku['head'][0] == board['height'] - 1:
                        if abs(sneku['head'][1] - self.head[1]) >= 2:
                            tmpHead = [sneku['head'][1] - 1, sneku['head'][1]]
                            if tmpHead in self.body:
                                #Okay, now we know we can kill the other sneku. Will we die if we do?
                                newHead = (board['height'] - 1, self.head[1])
                                headToTuna = self.astar(nmap, newHead, tuna)
                                
                                if headToTuna:
                                    self.lastMove = [1, 0]
                                    return [1, 0]
                                    
            #Right wall
            if self.body[-1][1] == board['width'] - 2 and self.body[-2][1] == board['width'] - 2 and self.body[-3][1] == board['width'] - 2:
                for colour, sneku in board['snekus'].iteritems():
                    if colour == self.colour:
                        continue
                        
                    if sneku['head'][1] == board['width'] - 1:
                        if abs(sneku['head'][0] - self.head[0]) >= 2:
                            tmpHead = [sneku['head'][0], sneku['head'][1] - 1]
                            if tmpHead in self.body:
                                #Okay, now we know we can kill the other sneku. Will we die if we do?
                                newHead = (self.head[0], board['width'] - 1)
                                headToTuna = self.astar(nmap, newHead, tuna)
                                
                                if headToTuna:
                                    self.lastMove = [0, 1]
                                    return [0, 1]
             
            #Left wall
            if self.body[-1][1] == 1 and self.body[-2][1] == 1 and self.body[-3][1] == 1:
                for colour, sneku in board['snekus'].iteritems():
                    if colour == self.colour:
                        continue
                        
                    if sneku['head'][1] == 0:
                        if abs(sneku['head'][0] - self.head[0]) >= 2:
                            tmpHead = [sneku['head'][0], sneku['head'][1] + 1]
                            if tmpHead in self.body:
                                #Okay, now we know we can kill the other sneku. Will we die if we do?
                                newHead = (self.head[0], 0)
                                headToTuna = self.astar(nmap, newHead, tuna)
                                
                                if headToTuna:
                                    self.lastMove = [0, -1]
                                    return [0, -1]                   
        
        headToTuna = self.astar(nmap, head, tuna)
        headToTail = self.astar(tunaMap, head, tail)
        tunaToTail = self.astar(tunaMap, tuna, tail)
        
        if tunaToTail:
            if headToTuna:
                nextMove = headToTuna[-1]
                print "1: %s" % headToTuna
            else:
                if headToTail:
                    nextMove = headToTail[-1]
                    print "2: %s" % headToTail
                else:
                    nextMove = [self.head[0] + self.lastMove[0], self.head[1] + self.lastMove[1]]
                    print "3: %s" % self.lastMove
        else:
            if headToTuna and len(headToTuna) == 1:
                nextMove = headToTuna[-1]
                print "4: %s" % headToTuna
            else:
                if headToTail:
                    nextMove = headToTail[-1]
                    print "5: %s" % headToTail
                else:
                    if headToTuna:
                        nextMove = headToTuna[-1]
                        print "6: %s" % headToTuna
                    else:
                        nextMove = [self.head[0] + self.lastMove[0], self.head[1] + self.lastMove[1]]
                        print "7: %s" % self.lastMove
            
        move = [0,0]
        move[0] = nextMove[0] - self.head[0]
        move[1] = nextMove[1] - self.head[1]
        
        if not self.sanityCheckMove(move):            
            for m in [[0,1],[0,-1],[1,0],[-1,0]]:
                if self.sanityCheckMove(m):
                    move = m
                    break

        self.lastMove = move
        return move
