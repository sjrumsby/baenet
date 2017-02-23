import Tkinter as tk
import tkMessageBox
from game import *
import yaml

class Battlesneku:
	
    def __init__(self, master, snekNames, numSnakes, colours, appleMax, appleRate):
        self.state = 0
        self.numSnakes = numSnakes
        self.game = Game(snekNames, 17, 17, appleMax, appleRate)
        self.tile_plain = tk.PhotoImage(file = "images/plain.gif")
        self.tile_apple = tk.PhotoImage(file = "images/apple.gif")
        self.snekuSelfie = tk.PhotoImage(file="images/snek.gif")
        
        #All of the different directions and colour images
        self.colours = colours
        self.snekTiles = {}
        self.sneks = {}
        
        for i in range(self.numSnakes):
            self.snekTiles[self.colours[i]] = {}
            self.snekTiles[self.colours[i]]["start"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuBody_start.gif"),
            self.snekTiles[self.colours[i]]["horizontal"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuBody_across.gif"),
            self.snekTiles[self.colours[i]]["vertical"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuBody_up.gif"),
            self.snekTiles[self.colours[i]]["rightUp"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuBody_rightUp.gif"),
            self.snekTiles[self.colours[i]]["rightDown"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuBody_rightDown.gif"),
            self.snekTiles[self.colours[i]]["leftUp"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuBody_leftUp.gif"),
            self.snekTiles[self.colours[i]]["leftDown"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuBody_leftDown.gif"),
            self.snekTiles[self.colours[i]]["endUp"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuHead_up.gif"),
            self.snekTiles[self.colours[i]]["endDown"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuHead_down.gif"),
            self.snekTiles[self.colours[i]]["endLeft"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuHead_left.gif"),
            self.snekTiles[self.colours[i]]["endRight"] = tk.PhotoImage(file = "images/" + self.colours[i] + "/snekuHead_right.gif")
            
            self.sneks[self.colours[i]] = {}
            
        snekuStatusBar = tk.Frame(master).grid(row=0)
        master.grid_columnconfigure(1, weight=1)
        #master.grid_columnconfigure(1, weight=1)
        #master.grid_columnconfigure(self.game.width+2, weight=1)
        master.grid_columnconfigure(self.game.width+3, weight=1)

        tk.Label(snekuStatusBar, text="Life").grid(row=0, column=0, columnspan=2)
        
        for i in range(self.numSnakes):
            colourLabel = tk.Label(snekuStatusBar, text=self.colours[i])
            colourLabel.grid(row=1+i, column=0, columnspan=1)
            self.sneks[self.colours[i]]["lifeLabel"] = tk.Label(snekuStatusBar, text="100", width=3)
            self.sneks[self.colours[i]]["lifeLabel"].grid(row=1+i, column=1, columnspan=1)

        distinguishedSneku = tk.Button(snekuStatusBar, image=self.snekuSelfie, command=self.startGame)
        distinguishedSneku.photo = self.snekuSelfie
        distinguishedSneku.grid(row=0, column=2, columnspan=self.game.width, rowspan=1+self.numSnakes)

        tk.Label(snekuStatusBar, text="Score").grid(row=0, column=2+self.game.width, columnspan=2)
        for i in range(self.numSnakes):
            scoreLabel = tk.Label(snekuStatusBar, text=self.colours[i])
            scoreLabel.grid(row=1+i, column=2+self.game.width, columnspan=1)
            self.sneks[self.colours[i]]["scoreLabel"] = tk.Label(snekuStatusBar, text="0")
            self.sneks[self.colours[i]]["scoreLabel"].grid(row=1+i, column=3+self.game.width, columnspan=1)

        tk.Label(text="").grid(row=1+self.numSnakes, column=0, columnspan=4+self.game.width)
        self.snekuFrame = tk.Frame(master).grid(row=2+self.numSnakes)

        rowOffset = 2 + self.numSnakes
        columnOffset = 2

        for i in range(self.game.height):
            for j in range(self.game.width):
                tile = tk.Label(self.snekuFrame, image=self.tile_plain, borderwidth=0)
                tile.photo = self.tile_plain
                tile.grid(row=rowOffset+i, column=columnOffset+j)
                self.game.grid[i][j].label = tile
                
        self.snekuRights = tk.Label(text="Copyright 2017 Baenet Industries").grid(row=rowOffset+self.game.height, column=0, columnspan=4+self.game.width)
		
    def startGame(self):
        if self.state:
            print "Hungry sneku in feeding. Don't mess with hungry snekus!"
            return

        print "Starting game..."
        self.state = 1
        self.game.resetGame()
        self.game.initGame(self.colours, self.numSnakes)
        self.updateCells()

    def endGame(self):
        self.state = 0

    def updateCells(self):
        if not self.state:
            return
            
        #Build the grid so we know which cells have been drawn
        grid = []
        for i in range(self.game.height):
            row = []
            for j in range(self.game.width):
                row.append(0)
            grid.append(row)
        
        #Add the apples
        for apple in self.game.apples:
            self.game.grid[apple[0]][apple[1]].updateCell(self.tile_apple)
            grid[apple[0]][apple[1]] = 1
        
        #Add the snake
        for sneku in [x for x in self.game.snekus if x.dead == 0]:
            
            if len(sneku.body) == 1:
                self.game.grid[sneku.head[0]][sneku.head[1]].updateCell(self.snekTiles[sneku.colour]["start"])
                grid[sneku.head[0]][sneku.head[1]] = 1
            elif len(sneku.body) == 2:
                direction = [sneku.body[1][0] - sneku.body[0][0], sneku.body[1][1] - sneku.body[0][1]]
                #Going up
                if direction == [-1,0]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.snekTiles[sneku.colour]["vertical"])
                    self.game.grid[sneku.body[1][0]][sneku.body[1][1]].updateCell(self.snekTiles[sneku.colour]["endUp"])
                #Going down
                elif direction == [1,0]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.snekTiles[sneku.colour]["vertical"])
                    self.game.grid[sneku.body[1][0]][sneku.body[1][1]].updateCell(self.snekTiles[sneku.colour]["endDown"])
                #Going left
                elif direction == [0,-1]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.snekTiles[sneku.colour]["horizontal"])
                    self.game.grid[sneku.body[1][0]][sneku.body[1][1]].updateCell(self.snekTiles[sneku.colour]["endLeft"])
                #Going right
                elif direction == [0,1]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.snekTiles[sneku.colour]["horizontal"])
                    self.game.grid[sneku.body[1][0]][sneku.body[1][1]].updateCell(self.snekTiles[sneku.colour]["endRight"])
                    
                else:
                    print "This shouldn't be possible..."
                    self.endGame()
                    
                grid[sneku.body[0][0]][sneku.body[0][1]] = 1
                grid[sneku.body[1][0]][sneku.body[1][1]] = 1
            else:
                initDirection = [sneku.body[0][0] - sneku.body[1][0], sneku.body[0][1] - sneku.body[1][1]]
                if initDirection == [-1,0]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.snekTiles[sneku.colour]["endUp"])
                elif initDirection == [1,0]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.snekTiles[sneku.colour]["endDown"])
                elif initDirection == [0,-1]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.snekTiles[sneku.colour]["endLeft"])
                elif initDirection == [0,1]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.snekTiles[sneku.colour]["endRight"])
                
                grid[sneku.body[0][0]][sneku.body[0][1]] = 1
                    
                for s in range(1, len(sneku.body) - 1):
                    moves = [[sneku.body[s][0] - sneku.body[s-1][0], sneku.body[s][1] - sneku.body[s-1][1]],[sneku.body[s+1][0] - sneku.body[s][0], sneku.body[s+1][1] - sneku.body[s][1]]]
                    
                    if moves == [[1,0],[1,0]] or moves == [[-1,0],[-1,0]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.snekTiles[sneku.colour]["vertical"])
                        
                    elif moves == [[0,1],[0,1]] or moves == [[0,-1],[0,-1]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.snekTiles[sneku.colour]["horizontal"])
                        
                    elif moves == [[-1,0],[0,-1]] or moves == [[0,1],[1,0]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.snekTiles[sneku.colour]["leftDown"])
                        
                    elif moves == [[-1,0],[0,1]] or moves == [[0,-1],[1,0]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.snekTiles[sneku.colour]["rightDown"])
                        
                    elif moves == [[0,1],[-1,0]] or moves == [[1,0],[0,-1]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.snekTiles[sneku.colour]["leftUp"])
                        
                    elif moves == [[0,-1],[-1,0]] or moves == [[1,0],[0,1]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.snekTiles[sneku.colour]["rightUp"])
                        
                    grid[sneku.body[s][0]][sneku.body[s][1]] = 1
                    
                headDirection = [sneku.body[-1][0] - sneku.body[-2][0], sneku.body[-1][1] - sneku.body[-2][1]]
                if headDirection == [-1,0]:
                    self.game.grid[sneku.body[-1][0]][sneku.body[-1][1]].updateCell(self.snekTiles[sneku.colour]["endUp"])
                #Going down
                elif headDirection == [1,0]:
                    self.game.grid[sneku.body[-1][0]][sneku.body[-1][1]].updateCell(self.snekTiles[sneku.colour]["endDown"])
                #Going left
                elif headDirection == [0,-1]:
                    self.game.grid[sneku.body[-1][0]][sneku.body[-1][1]].updateCell(self.snekTiles[sneku.colour]["endLeft"])
                #Going right
                elif headDirection == [0,1]:
                    self.game.grid[sneku.body[-1][0]][sneku.body[-1][1]].updateCell(self.snekTiles[sneku.colour]["endRight"])
                    
                grid[sneku.body[-1][0]][sneku.body[-1][1]] = 1
                        
        #Set evertyhing else to black
        for i in range(self.game.height):
            for j in range(self.game.width):
                if grid[i][j] == 0:
                    self.game.grid[i][j].updateCell(self.tile_plain)
		
        for sneku in self.game.snekus:
            self.sneks[sneku.colour]["lifeLabel"].configure(text=sneku.life)
            self.sneks[sneku.colour]["scoreLabel"].configure(text=sneku.score)
        
        stillHungry = 0
        for sneku in self.game.snekus:
            if sneku.dead == 0:
                stillHungry = 1
         
        if not stillHungry:
            if self.state == 1:
                tkMessageBox.showwarning("Game over", "Sneku dedded")
            self.state = 0

    def hssst(self):
        if self.state != 1:
            return
        
        self.game.makeMoves()
        self.game.updateBoard()
        self.updateCells()

config = yaml.safe_load(open("snektributes.yml"))

def Refresher(snekGame):
    snekGame.hssst()
    root.after(config['tickRate'], Refresher, snekGame)

root = tk.Tk()
root.title("Sneku Feeding!")

try:
    snekNames = config['snekNames']
except KeyError:
    snekNames = ["classic", "diagonal"]
    
try:
    numSnakes = config['numSnakes']
except KeyError:
    numSnakes = 6
    
try:
    colours = config['colours']
except KeyError:
    colours = ["white", "green", "blue", "yellow", "orange", "pink"]
    
try:
    appleMax = config['appleMax']
except KeyError:
    appleMax = 3
    
try:
    appleRate = config['appleRate']
except KeyError:
    appleRate = 10

snek = Battlesneku(root, snekNames, numSnakes, colours, appleMax, appleRate)
Refresher(snek)
root.mainloop()
