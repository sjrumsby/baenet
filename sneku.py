import numpy
from heapq import *

class Sneku:
    def __init__(self, x, y, colour, dimensions, apple):
        self.head = [x,y]
        self.body = [[x,y]]
        self.colour = colour
        self.dimensions = dimensions
        self.apple = apple
        self.length = 1
        self.life = 100
        self.score = 0
        self.dead = False
        self.lastMove = []
        self.lastTail = []
    
    def makeMove(self, board):
        self.apple = board["apple"]
        
        def heuristic(a, b):
            return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    
        def astar(array, start, goal):
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
                            continue
                    else:
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
            self.lastTail = self.body[0]
            self.body = self.body[1:]
        
        self.lastMove = move
        return move
        
    def sanityCheckMove(self, move):
        nextPos = [self.head[0] + move[0], self.head[1] + move[1]]
        
        if nextPos[0] < 0 or nextPos[0] >= self.dimensions[0]:
            print "(%s) Dont do that! You'll hit a wall!" % (self.colour)
            return False
        if nextPos[1] < 0 or nextPos[1] >= self.dimensions[1]:
            print "(%s) Dont do that! You'll hit a wall!" % (self.colour)
            return False
        if nextPos in self.body:
            print "(%s) Don't do that, you'll hit yourself!" % (self.colour)
            return False
            
        return True
        
    
    def eatApple(self, apple):
        self.length += 2
        self.life = 100
        self.score += 1
        self.apple = apple
        
    def killSneku(self):
        self.dead = True
