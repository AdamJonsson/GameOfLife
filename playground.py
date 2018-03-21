from cell import Cell

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
        

    def updatePlayground(self):
        """ 
            Updates the playground.
            :return: (nothing)
        """
        if(self.keyboard.spaceKey):
            self.updateCells()
        self.mouseInput()


    def mouseInput(self):
        """
            This method is getting the mouse and doing diffret thing with it. For example: spawning a new cell if the user click on an grid-box.
        """
        xPos = self.mouse.xGridPos
        yPos = self.mouse.yGridPos

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
            Delleting a cell from the cell-list.
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

    def updateCells(self):
        for cellIndex in range(len(self.cells)):
            cell = self.cells[cellIndex]
            xPos = cell.x 
            yPos = cell.y
            for indexX in range(xPos - 1, xPos + 2):
                for indexY in range(yPos - 1, yPos + 2):
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
            if(cell.x <= 0 or cell.y <= 0 or cell.x >= self.screen.worldSize or cell.y >= self.screen.worldSize):
                cellsToDelete.append(cell)
            elif(cell.numOfNeighbor > 3 or cell.numOfNeighbor < 2 or (cell.numOfNeighbor == 2 and cell.dead == True)):
                cellsToDelete.append(cell)
            elif(cell.numOfNeighbor == 3 and cell.dead == True):
                cell.makeAlive()
            cell.numOfNeighbor = 0

        for cell in cellsToDelete:
            cell.delete()
            self.cells.remove(cell)

