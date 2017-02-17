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
        
        return farthestPoint
    
    def playWithFood(self):
        #TODO: Figure out how to move around if we fucked up
        #Return false for now to keep moving in whatever direction we went last time
        return False
    
    def makeMove(self, board):
        def heuristic(a, b):
            return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    
        def astar(array, start, goal):
            print "Finding move from %s to %s" % (start, goal)
    
            neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
    
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
            
        nmap = numpy.array(grid)
        nextMove = astar(nmap, tuple(self.head), tuple(self.apple))
        
        if not nextMove:
            #If no path to apple exists, try to move around and hopefully one opens up
            nextMove = self.playWithFood()
            
            if not nextMove:
                nextMove = self.lastMove
            else:
                nextMove = nextMove[-1]
        else:
            nextMove = nextMove[-1]
            
        move = [0,0]
        move[0] = nextMove[0] - self.head[0]
        move[1] = nextMove[1] - self.head[1]
        print "Next move: %s" % move
        
        self.head[0] += move[0]
        self.head[1] += move[1]
        self.body.append(self.head[:])
        self.life -= 1
        if len(self.body) > self.length:
            self.body = self.body[1:]
        
        print "Moving: %s. Length: %s. Life: %s. Status : %s" % (move, self.length, self.life, self.dead)
        self.lastMove = move
        return move
        
    def eatApple(self, apple):
        print apple
        self.length += 2
        self.life = 100
        self.score += 1
        self.apple = apple
        
    def killSnake(self):
        self.dead = 1
