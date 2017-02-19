import numpy
from heapq import *

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
        self.lastMove = []
        self.lastTail = []
        
        #self.body = [[12, 6], [12, 5], [12, 4], [12, 3], [12, 2], [12, 1], [12, 0], [13, 0], [13, 1], [13, 2], [13, 3], [13, 4], [13, 5], [13, 6], [14, 6], [14, 7], [14, 8], [14, 9], [14, 10], [14, 11], [14, 12], [14, 13], [13, 13], [12, 13], [11, 13], [10, 13], [9, 13], [8, 13], [7, 13], [7, 14], [8, 14], [9, 14], [10, 14], [11, 14], [12, 14], [13, 14], [13, 15], [14, 15], [14, 16], [13, 16], [12, 16], [11, 16], [10, 16], [9, 16], [8, 16], [7, 16], [6, 16], [6, 15], [6, 14], [6, 13], [6, 12], [6, 11], [6, 10], [6, 9], [6, 8], [7, 8], [8, 8], [9, 8], [10, 8], [11, 8], [12, 8], [13, 8], [13, 7]]
        #self.length = len(self.body)
        
    
    def playWithFood(self):
        #TODO: Figure out how to move around if we fucked up
        #Return false for now to keep moving in whatever direction we went last time
        return False
    
    def makeMove(self, board):
        print "====="
        def heuristic(a, b):
            return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    
        def astar(array, start, goal):
            #print "Finding move from %s to %s" % (start, goal)
    
            neighbors = [(0,1),(1,0),(0,-1),(-1,0)]
    
            close_set = set()
            came_from = {}
            gscore = {start:0}
            fscore = {start:heuristic(start, goal)}
            oheap = []
    
            heappush(oheap, (fscore[start], start))
            
            while oheap:
                current = heappop(oheap)[1]
        
                if current == goal:
                    data = []
                    while current in came_from:
                        data.append(current)
                        current = came_from[current]
                    return data
        
                close_set.add(current)
                for i, j in neighbors:
                    neighbor = current[0] + i, current[1] + j            
                    tentative_g_score = gscore[current] + heuristic(current, neighbor)
                    if 0 <= neighbor[0] < array.shape[0]:
                        if 0 <= neighbor[1] < array.shape[1]:                
                            if array[neighbor[0]][neighbor[1]] == 1:
                                continue
                        else:
                            # array bound y walls
                            continue
                    else:
                        # array bound x walls
                        continue
                    
                    if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                        continue
                    
                    if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_g_score
                        fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heappush(oheap, (fscore[neighbor], neighbor))
                    
            return False
    
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
        
        tuna = tuple(self.apple)
        head = tuple(self.head)
        tail = tuple(self.body[0])
        
        tunaGrid = list(grid)
        tunaGrid[tail[0]][tail[1]] = 0
        
        nmap = numpy.array(grid)
        tunaMap = numpy.array(tunaGrid)
        
        headToTuna = astar(nmap, head, tuna)
        headToTail = astar(tunaMap, head, tail)
        tunaToTail = astar(tunaMap, tuna, tail)
        
        #print "Snake: %s" % self.body
        #print "Head: %s. Tail: %s. Apple: %s" % (self.head, self.body[0], self.apple)
        #print "Head to Tuna: %s" % headToTuna
        #print "Head to Tail: %s" % headToTail
        #print "Tuna to Tail: %s" % tunaToTail
        
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
            
        print nextMove
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
            self.lastTail = self.body[0]
            self.body = self.body[1:]
        
        print "Moving: %s. Length: %s. Life: %s. Status : %s" % (move, self.length, self.life, self.dead)
        self.lastMove = move
        return move
        
    def sanityCheckMove(self, move):
        nextPos = [self.head[0] + move[0], self.head[1] + move[1]]
        
        if nextPos[0] < 0 or nextPos[0] >= self.dimensions[0]:
            print "Dont do that! You'll hit a wall!"
            return False
        if nextPos[1] < 0 or nextPos[1] >= self.dimensions[1]:
            print "Dont do that! You'll hit a wall!"
            return False
        if nextPos in self.body:
            print "Don't do that, you'll hit yourself!"
            return False
            
        return True
        
    
    def eatApple(self, apple):
        print apple
        self.length += 2
        self.life = 100
        self.score += 1
        self.apple = apple
        
    def killSnake(self):
        self.dead = 1
