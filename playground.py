from cell import Cell
from tkinter import messagebox
import time
import fileTools

class Playground:

	"""
		The playground for the program. All cells are stored here. This object also import/export cells to the playground

		:param screen: The screen object.
		:param mouse: The mouse object.
		:param keyboard: The keyboard object.
		:param root: The root object.

		Attributes: 
		cells: All the cells that is on the playground. 
		clickSwitch: The size of the one grid box in pixels.
	"""

	def __init__(self, root, screen, mouse, keyboard):
		self.root = root
		self.screen = screen
		self.mouse = mouse
		self.keyboard = keyboard
		self.cells = []

		self.clickSwitch = False
		self.autoGenerateMode = False
		self.generation = 0
		self.timeToCalcGeneration = 0

		self.bindKeyboardKeysToFunctions()

	
	def bindKeyboardKeysToFunctions(self):
		""" 
			Binds diffrent functions to keyboard presses. 
			:return: (nothing)
		"""
		self.keyboard.bindFunctionToKey("space", self.nextGeneration)


	def updatePlayground(self):
		""" 
			Updates the playground. Checking for user input to interact with the playground.
			:return: (nothing)
		"""
		self.getMouseInput()
		if(self.autoGenerateMode):
			self.nextGeneration()


	def getMouseInput(self):
		"""
			This method is getting the mouse and doing diffret thing with it. For example: spawning a new cell if the user click on an grid-box.
			:return: (nothing)
		"""
		xPos = self.mouse.xGridPos
		yPos = self.mouse.yGridPos

		if(self.getCellFromPosition(xPos, yPos)):
			self.screen.canvas.itemconfig(self.screen.hoverBlock, fill='#ff0000')
		else:
			self.screen.canvas.itemconfig(self.screen.hoverBlock, fill='#00ff00')

		if(self.mouse.leftButton and self.clickSwitch == False):
			if(self.keyboard.shiftKey):
				clickedCell = self.getCellFromPosition(xPos, yPos)
				if(clickedCell == False):
					self.createCell(xPos, yPos)
				else:
					self.deleteCell(clickedCell)
			self.clickSwitch = True

		if (self.mouse.leftButton == False and self.clickSwitch == True):

			self.clickSwitch = False


	def deleteCell(self, cell):
		"""
			Deleting a cell from the cell-list.
			:param cell: The cell that is going to be delete.
			:return: (nothing)
		"""
		index = self.cells.index(cell)
		self.cells[index].delete()
		self.cells.remove(cell)


	def createCell(self, xPos, yPos):
		"""
			Creates a new cell for a given position.
			:param xPos: The x-position on the grid.
			:param yPos: the y-position on the grid
			:return: (nothing)
		"""
		self.cells.append(Cell(self.screen, xPos, yPos))


	def getCellFromPosition(self, xPos, yPos):
		"""
			Gets a cell from a given position.
			:param xPos: The x-position on the grid.
			:param yPos: the y-position on the grid
			:return: Cell
		"""
		for cell in self.cells:
			if(xPos == cell.x and yPos == cell.y):
				return cell
		return False


	def clearPlayground(self):
		"""
			Removes all the cells from the playground
			:return: (nothing)
		"""

		for cell in self.cells:
			cell.delete()
		self.cells = []
		self.generation = 0


	def importPlayground(self, filepath):
		"""
			This function is importing a playground.
			:param filepath: The filepath to import the playground to. 
			:return: (nothing)
		"""

		cellOutOfBound = False
		avgXPos = 0
		avgYPos = 0
		fileWrite = open(filepath, "r")
		cellPositions = fileWrite.readlines()

		self.clearPlayground()
		
		for cellPos in cellPositions:

			cleanCellPos = fileTools.cleanString(cellPos)
			if(cleanCellPos == ""):
				continue

			try:
				cellPosList = cleanCellPos.split()
				cellXPos = int(cellPosList[0])
				cellYPos = int(cellPosList[1])
			except ValueError:
				messagebox.showerror("Error: Wrong format", "The choosen file do not have the correct format. Be so kind to choose an other file.")
				return

			if(cellXPos > self.screen.worldSize or cellYPos > self.screen.worldSize or cellXPos < 0 or cellYPos < 0):
				cellOutOfBound = True
			else:
				newCell = Cell(self.screen, cellXPos, cellYPos)
				rectCellPos = self.screen.canvas.coords(newCell.rect)
				avgXPos += rectCellPos[0]; avgYPos += rectCellPos[1]

				self.cells.append(newCell)

		if(cellOutOfBound):
			messagebox.showwarning("Warning!", "Some cells are placed outside of the playground!")

			


		#Moving the user to where the cells are.
		avgXPos /= len(cellPositions); avgYPos /= len(cellPositions)
		self.screen.offsetX += avgXPos - self.screen.width/2
		self.screen.offsetY += avgYPos - self.screen.height/2


	def exportPlayground(self, filepath):
		"""
			This function is exporting a playground.
			:param filepath: The filepath to export the playground to. 
			:return: (nothing)
		"""
		cellPositions = ""
		for cell in self.cells:
			if(cell.dead == False):
				cellPositions += str(cell.x) + " " + str(cell.y) + "\n"
		
		fileWrite = open(filepath, "w")
		fileWrite.write(cellPositions)
		fileWrite.close()
		

	def checkFileFormat(self, fileContent):
		"""
			Checks if the file has the right format for this program.
			:param fileContent: The content of the file
			:return: True if the file content is correct, false if not.
		"""
		pass


	def removeCells(self, cellArray):
		"""
			Deletes all the cells from the array and playground.
			:param cellArray: The array of cells to delete.
			:return: (nothing)
		"""
		for cell in cellArray:
			cell.delete()
			self.cells.remove(cell)


	def nextGeneration(self):
		"""
			This method is updating the cells to the next generation.
			:return: (nothing)

			Thanks to Martins for the idea to have modolu of the current posotion.
		"""

		startTime = int(round(time.time() * 100000))

		self.generation += 1

		for cellIndex in range(len(self.cells)):
			cell = self.cells[cellIndex]
			xPos = cell.x
			yPos = cell.y
			for indexX in range(xPos - 1, xPos + 2):
				for indexY in range(yPos - 1, yPos + 2):
					indexX = indexX % self.screen.worldSize
					indexY = indexY % self.screen.worldSize
					if(indexX == xPos and indexY == yPos):
						continue
					else:
						cellToCheck = self.getCellFromPosition(indexX, indexY)
						if(cellToCheck != False):
							cellToCheck.numOfNeighbor += 1
						else:
							newCell = Cell(self.screen, indexX, indexY, True)
							newCell.numOfNeighbor += 1
							self.cells.append(newCell)

		cellsToDelete = []
		for cell in self.cells:
			if(cell.numOfNeighbor > 3 or cell.numOfNeighbor < 2 or (cell.numOfNeighbor == 2 and cell.dead == True)):
				cellsToDelete.append(cell)
			elif(cell.numOfNeighbor == 3 and cell.dead == True):
				cell.makeAlive()
			cell.numOfNeighbor = 0

		self.removeCells(cellsToDelete)

		endTime = int(round(time.time() * 100000))
		self.timeToCalcGeneration = (endTime - startTime)
