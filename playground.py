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
            This method is getting the mouse and doing diffrent thing with it. For example: spawning a new cell if the user click on an grid-box.
            :return: (nothing)
        """
        xPos = self.mouse.xGridPos
        yPos = self.mouse.yGridPos

        #Changing the hoverblock color depending if the mouse is hovering over an living cell or not.
        if(self.getCellFromPosition(xPos, yPos)):
            self.screen.canvas.itemconfig(self.screen.hoverBlock, fill='#ff0000')
        else:
            self.screen.canvas.itemconfig(self.screen.hoverBlock, fill='#00ff00')

        #Placing an cell on the playground if the user is clicking on the playground
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

            #Cleans the string
            cleanCellPos = fileTools.cleanString(cellPos)
            if(cleanCellPos == ""):
                continue

            #Check the format.
            cleanCellPos = self.checkFileFormat(cleanCellPos)
            if(cleanCellPos):
                cellXPos, cellYPos = cleanCellPos
            else:
                return

            #Checks if the coords is outside the world.
            if(cellXPos > self.screen.worldSize or cellYPos > self.screen.worldSize or cellXPos < 0 or cellYPos < 0):
                cellOutOfBound = True
            else:
                newCell = Cell(self.screen, cellXPos, cellYPos)
                rectCellPos = self.screen.canvas.coords(newCell.rect)
                avgXPos += rectCellPos[0]; avgYPos += rectCellPos[1]

                self.cells.append(newCell)

        #Print warning that some cells are not renderd.
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
        

    def checkFileFormat(self, cellPos):
        """
            Checks if the file has the right format for this program.
            :param fileContent: The content of the file
            :return: The positions in a tuple, (x, y), false if there is an error.
        """
        try:
            cellPosList = cellPos.split()
            cellXPos = int(cellPosList[0])
            cellYPos = int(cellPosList[1])
        except ValueError:
            messagebox.showerror("Error: Wrong format", "The choosen file do not have the correct format. Be so kind to choose an other file.")
            return False
        pass

        return (cellXPos, cellYPos)


    def removeCells(self, cellArray):
        """
            Deletes all the cells from the array and playground.
            :param cellArray: The array of cells to delete.
            :return: (nothing)
        """
        for cell in cellArray:
            cell.delete()
            self.cells.remove(cell)


    def setNeighbors(self):
        """
            Creates dead cells around all living cells and calculating all the neighbors for the dead and the living cells
            :return: (nothing)
        """
        for cellIndex in range(len(self.cells)):
            cell = self.cells[cellIndex]

            #Checks the 8 cells around the living one. 
            for neighborsX in range(cell.x - 1, cell.x + 2):
                for neighborsY in range(cell.y - 1, cell.y + 2):

                    #If the position is outside the world, loop around.
                    neighborsX = neighborsX % self.screen.worldSize
                    neighborsY = neighborsY % self.screen.worldSize

                    #Skipping itself. Becouse we do not want to calculate itself as a neighbor
                    if(neighborsX == cell.x and neighborsY == cell.y):
                        continue
                    else:
                        #Checks if a cell exist at neighborsX, neighborsY
                        cellToCheck = self.getCellFromPosition(neighborsX, neighborsY)
                        if(cellToCheck != False):
                            #Add one to the neighbor var if there already exist and cell for the given position.
                            cellToCheck.numOfNeighbor += 1
                        else:
                            #Creates a new cell if it do not exist any.
                            newCell = Cell(self.screen, neighborsX, neighborsY, True)
                            newCell.numOfNeighbor += 1
                            self.cells.append(newCell)


    def checkAmountOfNeighbors(self):
        """
            Check the amount of neighbors and kills or creates new cell depending on the amount.
            :return: (nothing)
        """
        cellsToDelete = []
        for cell in self.cells:
            if(cell.numOfNeighbor > 3 or cell.numOfNeighbor < 2 or (cell.numOfNeighbor == 2 and cell.dead == True)):
                cellsToDelete.append(cell)
            elif(cell.numOfNeighbor == 3 and cell.dead == True):
                cell.makeAlive()
            cell.numOfNeighbor = 0

        self.removeCells(cellsToDelete)

    def nextGeneration(self):
        """
            This method is updating the cells to the next generation.
            :return: (nothing)

            Thanks to Martins for the idea to have modolu of the current posotion.
        """

        # Start a timer to calculate the time the render one generation.
        startTime = int(round(time.time() * 100000))

        self.generation += 1

        self.setNeighbors()
        self.checkAmountOfNeighbors()

        # Ends a timer to calculate the time the render one generation.
        endTime = int(round(time.time() * 100000))
        self.timeToCalcGeneration = (endTime - startTime)
