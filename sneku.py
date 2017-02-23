from numpy import array as numpyArray
from heapq import *

class Sneku:
    def __init__(self, x, y, colour, dimensions):
        self.head = [x,y]
        self.body = [[x,y]]
        self.colour = colour
        self.dimensions = dimensions
        self.length = 1
        self.life = 100
        self.score = 0
        self.dead = False
        self.lastMove = []
        
    def heuristic(self, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])
    
    def astar(self, array, start, goal):
        neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

        close_set = set()
        came_from = {}
        gscore = {start:0}
        fscore = {start:self.heuristic(start, goal)}
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
                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)
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
                    fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(oheap, (fscore[neighbor], neighbor))
                
        return False

    def getClosestApple(self, board):
        apples = board["apples"]
        # Loop through apples and return close one to us
        closestApple = [0, 0]
        distance = 9999
        for apple in apples:
            currentDistance = self.heuristic(self.head, apple)
            if  currentDistance < distance:
                distance = currentDistance
                closestApple = apple
        if closestApple == [0, 0]: 
            print "No apple near us! Need to do further logic"
        return closestApple

    
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
        
    
    def eatApple(self):
        self.length += 2
        self.life = 100
        self.score += 1
        
    def killSneku(self):
        self.dead = True
