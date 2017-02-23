from numpy import array as numpyArray
from heapq import *
from sneku import *

class diagonalSneku(Sneku):
    def heuristic(self, a, b):
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    
    def makeMove(self, board):
        apple = self.getClosestApple(board)
        grid = []
        
        for row in range(board['height']):
            gridRow = []
            for col in range(board['width']):
                g = 0
                for sneku in board['snekus']:
                    for snekuBody in sneku:
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
        
        headToTuna = self.astar(nmap, head, tuna)
        headToTail = self.astar(tunaMap, head, tail)
        tunaToTail = self.astar(tunaMap, tuna, tail)
        
        if tunaToTail:
            if headToTuna:
                nextMove = headToTuna[-1]
            else:
                if headToTail:
                    nextMove = headToTail[-1]
                else:
                    nextMove = [self.head[0] + self.lastMove[0], self.head[1] + self.lastMove[1]]
        else:
            if headToTuna and len(headToTuna) == 1:
                nextMove = headToTuna[-1]
            else:
                if headToTail:
                    nextMove = headToTail[-1]
                else:
                    if headToTuna:
                        nextMove = headToTuna[-1]
                    else:
                        nextMove = [self.head[0] + self.lastMove[0], self.head[1] + self.lastMove[1]]
            
        move = [0,0]
        move[0] = nextMove[0] - self.head[0]
        move[1] = nextMove[1] - self.head[1]
        
        if not self.sanityCheckMove(move):            
            for m in [[0,1],[0,-1],[1,0],[-1,0]]:
                if self.sanityCheckMove(m):
                    move = m
                    break
        
        self.head[0] += move[0]
        self.head[1] += move[1]
        self.body.append(self.head[:])
        self.life -= 1
        
        if len(self.body) > self.length:
            self.body = self.body[1:]
        
        self.lastMove = move
        return move
        