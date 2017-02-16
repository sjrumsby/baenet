import Tkinter as tk
import random
from time import sleep

class Cell:
	def __init__(self, x, y):
		self.xpos = x
		self.ypos = y
		self.label = ""

class Game:
	def __init__(self):
		self.life = 100
		self.height = 8
		self.width = 8
		self.apple = []
		self.snake = []
		self.grid = []
		
		for i in range(self.height):
			row = []
			for j in range(self.width):
				c = Cell(i,j)
				
				if [i,j] in self.snake:
					c.content = 1
					
				if [i,j] == self.apple:
					c.content = -1
					
				row.append(c)
			self.grid.append(row)
			
	def printFrame(self):
		top = "+"
		for i in range(self.width):
			top += "-"
		top += "+"
		
		print top
		for i in range(self.height):
			row = "|"
			
			for j in range(self.width):
				if self.grid[i][j].content == -1:
					row += "a"
				elif self.grid[i][j].content == 0:
					row += " "
				elif self.grid[i][j].content == 1:
					row += "s"
				else:
					raise ValueError("Invalid cell content value: %s" % self.grid[i][j].content)
			row += "|"
			print row
			
		print top

class Sneku:
	
	def __init__(self, master):
		self.score = 0
		self.life = 100
		self.state = 0
		self.game = Game()
		self.tile_plain = tk.PhotoImage(file = "images/plain.gif")
		self.tile_head = tk.PhotoImage(file = "images/snekuBody.gif")
		self.tile_apple = tk.PhotoImage(file = "images/apple.gif")
		self.snekuSelfie = tk.PhotoImage(file="images/snek.gif")

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
		
		for i in range(3, 3 + self.game.height):
			for j in range(1, 1 + self.game.width):
				print i,j
				tile = tk.Label(self.snekuFrame, image=self.tile_plain, borderwidth=0)
				tile.photo = self.tile_plain
				tile.grid(row=i, column=j)
				self.game.grid[i-3][j-1].label = tile
				
		self.snekuRights = tk.Label(text="Copyright 2017 Baenet Industries").grid(row=3+self.game.height, column=0, columnspan=2+self.game.width)
		
	def startGame(self):
		if self.state:
			print "Hungry sneku in feeding. Don't mess with hungry snekus!"
			return
			
		print "Starting game..."
		self.state = 1
		counter = 0
		self.updateCells()
		print "Game over!"
		self.state = 0

	def updateCells(self):
		for row in self.game.grid:
			for cell in row:
				print cell.label.photo
		
	def increaseScore(self):
		self.score += 1
	
	def decreaseLife(self):
		self.life -= 1
	
	def setMaxLife(self):
		self.life = 100

root = tk.Tk()
root.title("Sneku Feeding!")

snek = Sneku(root)

root.mainloop()