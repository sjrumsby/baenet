import Tkinter as tk
from game import *
from time import sleep

class Battlesneku:
	
	def __init__(self, master):
		self.score = 0
		self.life = 100
		self.state = 0
		self.game = Game()
		self.tile_plain = tk.PhotoImage(file = "images/plain.gif")
		self.tile_body = tk.PhotoImage(file = "images/snekuBody.gif")
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
		print "Snake pos: %s" % self.game.snekus[0].body
		print "Apple pos: %s" % self.game.apple
		for row in self.game.grid:
			for cell in row:
				pos = [cell.x, cell.y]
				
				if pos == self.game.apple:
					print "Found an apple"
					cell.updateCell(self.tile_apple)
				elif pos in self.game.snekus[0].body:
					print "Found a snake"
					cell.updateCell(self.tile_body)
				else:
					cell.updateCell(self.tile_plain)
					
		print "Updated cells"
		
	def hssst(self):
		if self.state != 1:
			return
		
		for s in self.game.snekus:
			print "Make a move!"
			move = s.makeMove()
			print move
			
		self.updateCells()
		
	def increaseScore(self):
		self.score += 1
	
	def decreaseLife(self):
		self.life -= 1
	
	def setMaxLife(self):
		self.life = 100
		
def Refresher(snekGame):
    snekGame.hssst()
    root.after(1000, Refresher, snekGame)

root = tk.Tk()
root.title("Sneku Feeding!")

snek = Battlesneku(root)
Refresher(snek)
root.mainloop()
