from numpy import array as numpyArray
from heapq import *
from random import randint

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
        self.body = board["snekus"][self.colour]["body"]
        self.head = self.body[-1]
        moves = [[1,0], [-1,0], [0,1], [0,-1]]
        
        #Try 5 times to find something that works
        for i in range(5):
            r = randint(0,3)
            m = moves[r]
            if self.sanityCheckMove(m):
                return m
        
        #Otherwise snek it
        return m
        
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
        if nextPos == self.lastMove:
            return False
            
        return True
        
    
    def eatApple(self):
        self.length += 2
        self.life = 100
        self.score += 1
        
    def killSneku(self):
        self.dead = True
