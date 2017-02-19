import Tkinter as tk
import tkMessageBox
from game import *
from time import sleep, time

class Battlesneku:
	
    def __init__(self, master):
        self.state = 0
        self.game = Game()
        self.tile_plain = tk.PhotoImage(file = "images/plain.gif")
        self.tile_apple = tk.PhotoImage(file = "images/apple.gif")
        self.snekuSelfie = tk.PhotoImage(file="images/snek.gif")
        
        #All of the different directions
        self.tile_body_white_start = tk.PhotoImage(file = "images/white/snekuBody_start.gif")
        self.tile_body_white_across = tk.PhotoImage(file = "images/white/snekuBody_across.gif")
        self.tile_body_white_up = tk.PhotoImage(file = "images/white/snekuBody_up.gif")
        self.tile_body_white_rightUp = tk.PhotoImage(file = "images/white/snekuBody_rightUp.gif")
        self.tile_body_white_rightDown = tk.PhotoImage(file = "images/white/snekuBody_rightDown.gif")
        self.tile_body_white_leftUp = tk.PhotoImage(file = "images/white/snekuBody_leftUp.gif")
        self.tile_body_white_leftDown = tk.PhotoImage(file = "images/white/snekuBody_leftDown.gif")
        
        self.tile_head_white_up = tk.PhotoImage(file = "images/white/snekuHead_up.gif")
        self.tile_head_white_down = tk.PhotoImage(file = "images/white/snekuHead_down.gif")
        self.tile_head_white_left = tk.PhotoImage(file = "images/white/snekuHead_left.gif")
        self.tile_head_white_right = tk.PhotoImage(file = "images/white/snekuHead_right.gif")

        snekuStatusBar = tk.Frame(master).grid(row=0)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(self.game.width+1, weight=1)

        tk.Label(snekuStatusBar, text="Life").grid(row=0, column=0, columnspan=1)
        self.lifeLabel = tk.Label(snekuStatusBar, text="100")
        self.lifeLabel.grid(row=1, column=0, columnspan=1)

        distinguishedSneku = tk.Button(snekuStatusBar, image=self.snekuSelfie, command=self.startGame)
        distinguishedSneku.photo = self.snekuSelfie
        distinguishedSneku.grid(row=0, column=1, columnspan=self.game.width, rowspan=2)

        tk.Label(snekuStatusBar, text="Score").grid(row=0, column=1+self.game.width, columnspan=1)
        self.scoreLabel = tk.Label(snekuStatusBar, text="0")
        self.scoreLabel.grid(row=1, column=1+self.game.width, columnspan=1)

        tk.Label(text="").grid(row=2, column=0, columnspan=2+self.game.width)
        self.snekuFrame = tk.Frame(master).grid(row=2)

        rowOffset = 3
        columnOffset = 1

        for i in range(self.game.height):
            for j in range(self.game.width):
                tile = tk.Label(self.snekuFrame, image=self.tile_plain, borderwidth=0)
                tile.photo = self.tile_plain
                tile.grid(row=rowOffset+i, column=columnOffset+j)
                self.game.grid[i][j].label = tile
                
        self.snekuRights = tk.Label(text="Copyright 2017 Baenet Industries").grid(row=3+self.game.height, column=0, columnspan=2+self.game.width)
		
    def startGame(self):
        if self.state:
            print "Hungry sneku in feeding. Don't mess with hungry snekus!"
            return

        print "Starting game..."
        self.state = 1
        self.game.resetGame()
        self.game.initGame()
        self.updateCells()

    def endGame(self):
        self.state = 0

    def updateCells(self):
        print "Updating cells"
        
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
                self.game.grid[sneku.head[0]][sneku.head[1]].updateCell(self.tile_body_white_start)
                grid[sneku.head[0]][sneku.head[1]] = 1
            elif len(sneku.body) == 2:
                direction = [sneku.body[1][0] - sneku.body[0][0], sneku.body[1][1] - sneku.body[0][1]]
                #Going up
                if direction == [-1,0]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.tile_body_white_up)
                    self.game.grid[sneku.body[1][0]][sneku.body[1][1]].updateCell(self.tile_head_white_up)
                #Going down
                elif direction == [1,0]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.tile_body_white_up)
                    self.game.grid[sneku.body[1][0]][sneku.body[1][1]].updateCell(self.tile_head_white_down)
                #Going left
                elif direction == [0,-1]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.tile_body_white_across)
                    self.game.grid[sneku.body[1][0]][sneku.body[1][1]].updateCell(self.tile_head_white_left)
                #Going right
                elif direction == [0,1]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.tile_body_white_across)
                    self.game.grid[sneku.body[1][0]][sneku.body[1][1]].updateCell(self.tile_head_white_right)
                    
                else:
                    print "This shouldn't be possible..."
                    self.endGame()
                    
                grid[sneku.body[0][0]][sneku.body[0][1]] = 1
                grid[sneku.body[1][0]][sneku.body[1][1]] = 1
            else:
                initDirection = [sneku.body[0][0] - sneku.body[1][0], sneku.body[0][1] - sneku.body[1][1]]
                if initDirection == [-1,0]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.tile_head_white_up)
                elif initDirection == [1,0]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.tile_head_white_down)
                elif initDirection == [0,-1]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.tile_head_white_left)
                elif initDirection == [0,1]:
                    self.game.grid[sneku.body[0][0]][sneku.body[0][1]].updateCell(self.tile_head_white_right)
                
                grid[sneku.body[0][0]][sneku.body[0][1]] = 1
                    
                for s in range(1, len(sneku.body) - 1):
                    moves = [[sneku.body[s][0] - sneku.body[s-1][0], sneku.body[s][1] - sneku.body[s-1][1]],[sneku.body[s+1][0] - sneku.body[s][0], sneku.body[s+1][1] - sneku.body[s][1]]]
                    
                    if moves == [[1,0],[1,0]] or moves == [[-1,0],[-1,0]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.tile_body_white_up)
                        
                    elif moves == [[0,1],[0,1]] or moves == [[0,-1],[0,-1]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.tile_body_white_across)
                        
                    elif moves == [[-1,0],[0,-1]] or moves == [[0,1],[1,0]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.tile_body_white_leftDown)
                        
                    elif moves == [[-1,0],[0,1]] or moves == [[0,-1],[1,0]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.tile_body_white_rightDown)
                        
                    elif moves == [[0,1],[-1,0]] or moves == [[1,0],[0,-1]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.tile_body_white_leftUp)
                        
                    elif moves == [[0,-1],[-1,0]] or moves == [[1,0],[0,1]]:
                        self.game.grid[sneku.body[s][0]][sneku.body[s][1]].updateCell(self.tile_body_white_rightUp)
                        
                    grid[sneku.body[s][0]][sneku.body[s][1]] = 1
                    
                headDirection = [sneku.body[-1][0] - sneku.body[-2][0], sneku.body[-1][1] - sneku.body[-2][1]]
                if headDirection == [-1,0]:
                    self.game.grid[sneku.body[-1][0]][sneku.body[-1][1]].updateCell(self.tile_head_white_up)
                #Going down
                elif headDirection == [1,0]:
                    self.game.grid[sneku.body[-1][0]][sneku.body[-1][1]].updateCell(self.tile_head_white_down)
                #Going left
                elif headDirection == [0,-1]:
                    self.game.grid[sneku.body[-1][0]][sneku.body[-1][1]].updateCell(self.tile_head_white_left)
                #Going right
                elif headDirection == [0,1]:
                    self.game.grid[sneku.body[-1][0]][sneku.body[-1][1]].updateCell(self.tile_head_white_right)
                    
                grid[sneku.body[-1][0]][sneku.body[-1][1]] = 1
                        
        #Set evertyhing else to black
        for i in range(self.game.height):
            for j in range(self.game.width):
                if grid[i][j] == 0:
                    self.game.grid[i][j].updateCell(self.tile_plain)
					
		self.lifeLabel.configure(text=self.game.snekus[0].life)
		self.scoreLabel.configure(text=self.game.snekus[0].score)
        
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
        
        for s in self.game.snekus:
            move_st = time()
            move = s.makeMove(self.game.getBoard())
            move_et = time()
        
        board_st = time()
        self.game.updateBoard()
        board_et = time()
        
        cells_st = time()
        self.updateCells()
        cells_et = time()
        
        moves_time = move_et - move_st
        board_time = board_et - board_st
        cells_time = cells_et - cells_st
        total_time = moves_time + board_time + cells_time
        
        #print "Total: %s. Move: %s. Board %s. Cells: %s" % (total_time, moves_time, board_time, cells_time)
		
def Refresher(snekGame):
    snekGame.hssst()
    root.after(50, Refresher, snekGame)

root = tk.Tk()
root.title("Sneku Feeding!")

snek = Battlesneku(root)
Refresher(snek)
root.mainloop()
