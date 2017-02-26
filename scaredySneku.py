from numpy import array as numpyArray
from heapq import *
from sneku import *

class scaredySneku(Sneku):
    def getType(self):
        return "scaredy"
        
    def heuristic(self, a, b):
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    
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
        
        # Check if we are touching a wall
        touchingWall = False
        if self.head[1] == 0:
            touchingWall = "left"
        elif self.head[0] == 0:
            touchingWall = "top";
        elif self.head[1] == board['height']-1:
            touchingWall = "right";
        elif self.head[0] == board['width']-1:
            touchingWall = "bottom"

        # If bottom left corner, the if order fuck us, so set wall to bottom
        if self.head[0] == board['height']-1 and self.head[1] == 0:
            touchingWall = "bottom"

        print "ScaredySnek touching wall: %s\n" % touchingWall

        # If not touchin a wall, find the nearest wall
        if touchingWall == False:
            distanceToLeftWall = self.head[1]
            distanceToBottomWall = board['width'] - self.head[0]
            distanceToRightWall = board['width'] - self.head[1]
            distanceToTopWall = self.head[0]

            # Ignore this spaghetti
            if distanceToTopWall > distanceToBottomWall and distanceToTopWall > distanceToLeftWall and distanceToTopWall > distanceToRightWall:
                move = [-1,0]
            elif distanceToBottomWall > distanceToLeftWall and distanceToBottomWall > distanceToRightWall and distanceToBottomWall > distanceToTopWall:
                move = [1,0]
            elif distanceToRightWall > distanceToLeftWall and distanceToRightWall > distanceToLeftWall and distanceToTopWall > distanceToBottomWall:
                move = [0,1]
            elif distanceToLeftWall > distanceToRightWall and distanceToLeftWall > distanceToBottomWall and distanceToLeftWall > distanceToTopWall:
                move = [0,-1]
            else:
                # Doesnt matter which direction, so continue
                move = self.lastMove
            self.lastMove = move
            return move

        # If we are, determine which wall we are touching and continue along 
        if touchingWall == "top":
            move = [0,-1]
        elif touchingWall == "right":
            move = [-1,0]
        elif touchingWall == "bottom":
            move = [0,1]
        elif touchingWall == "left":
            move = [1,0]

        self.lastMove = move
        return move
            
        