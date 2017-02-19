import Tkinter as tk
import tkMessageBox
from game import *
from time import sleep, time

class Battlesneku:
	
    def __init__(self, master):
        self.state = 0
        self.numSnakes = 6
        self.game = Game(17,17)
        self.tile_plain = tk.PhotoImage(file = "images/plain.gif")
        self.tile_apple = tk.PhotoImage(file = "images/apple.gif")
        self.snekuSelfie = tk.PhotoImage(file="images/snek.gif")
        
        #All of the different directions and colour images
        self.colours = ["white", "green", "blue", "yellow", "orange", "pink"]
        self.snekTiles = {}
        self.sneks = {}
        
        for c in self.colours:
            self.snekTiles[c] = {}
            self.snekTiles[c]["start"] = tk.PhotoImage(file = "images/" + c + "/snekuBody_start.gif"),
            self.snekTiles[c]["horizontal"] = tk.PhotoImage(file = "images/" + c + "/snekuBody_across.gif"),
            self.snekTiles[c]["vertical"] = tk.PhotoImage(file = "images/" + c + "/snekuBody_up.gif"),
            self.snekTiles[c]["rightUp"] = tk.PhotoImage(file = "images/" + c + "/snekuBody_rightUp.gif"),
            self.snekTiles[c]["rightDown"] = tk.PhotoImage(file = "images/" + c + "/snekuBody_rightDown.gif"),
            self.snekTiles[c]["leftUp"] = tk.PhotoImage(file = "images/" + c + "/snekuBody_leftUp.gif"),
            self.snekTiles[c]["leftDown"] = tk.PhotoImage(file = "images/" + c + "/snekuBody_leftDown.gif"),
            self.snekTiles[c]["endUp"] = tk.PhotoImage(file = "images/" + c + "/snekuHead_up.gif"),
            self.snekTiles[c]["endDown"] = tk.PhotoImage(file = "images/" + c + "/snekuHead_down.gif"),
            self.snekTiles[c]["endLeft"] = tk.PhotoImage(file = "images/" + c + "/snekuHead_left.gif"),
            self.snekTiles[c]["endRight"] = tk.PhotoImage(file = "images/" + c + "/snekuHead_right.gif")
            
            self.sneks[c] = {}
            
        snekuStatusBar = tk.Frame(master).grid(row=0)
        master.grid_columnconfigure(0, weight=1)
        #master.grid_columnconfigure(1, weight=1)
        #master.grid_columnconfigure(self.game.width+2, weight=1)
        master.grid_columnconfigure(self.game.width+3, weight=1)

        tk.Label(snekuStatusBar, text="Life").grid(row=0, column=0, columnspan=2)
        
        for i in range(self.numSnakes):
            colourLabel = tk.Label(snekuStatusBar, text=self.colours[i])
            colourLabel.grid(row=1+i, column=0, columnspan=1)
            self.sneks[self.colours[i]]["lifeLabel"] = tk.Label(snekuStatusBar, text="100")
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
        
        #Add the apple
        self.game.grid[self.game.apple[0]][self.game.apple[1]].updateCell(self.tile_apple)
        grid[self.game.apple[0]][self.game.apple[1]] = 1
        
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
        
        for sneku in self.game.snekus:
            if sneku.dead == False:
                move = sneku.makeMove(self.game.getBoard())
        
        self.game.updateBoard()
        self.updateCells()

		
def Refresher(snekGame):
    snekGame.hssst()
    root.after(75, Refresher, snekGame)

root = tk.Tk()
root.title("Sneku Feeding!")

snek = Battlesneku(root)
Refresher(snek)
root.mainloop()
