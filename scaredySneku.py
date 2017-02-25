from numpy import array as numpyArray
from heapq import *
from sneku import *

class scaredySneku(Sneku):
    def getType(self):
        return "scaredy"
        
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
        
    def makeMove(self, board):
        self.body = board["snekus"][self.colour]["body"]
        self.head = self.body[-1]
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
        
        if self.heuristic(self.head, apple) <= (1+ 50/self.life):
            tuna = tuple(apple)
            head = tuple(self.head)
            tunaGrid = list(grid)
            nmap = numpyArray(grid)
            
            headToTuna = self.astar(nmap, head, tuna)
            nextMove = headToTuna[-1]
            move = [nextMove[0] - self.head[0], nextMove[1] - self.head[1]]
            return move
        else:
            moves = [[1,0], [-1,0], [0,1], [0,-1]]
        
            #Try 5 times to find something that works
            for i in range(5):
                r = randint(0,3)
                m = moves[r]
                if self.sanityCheckMove(m):
                    return m
            
            #Otherwise snek it
            return m
            