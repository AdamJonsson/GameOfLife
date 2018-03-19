from cell import Cell

class Playground:

    def __init__(self, root, screen, mouse, keyboard):
        self.root = root
        self.screen = screen
        self.mouse = mouse
        self.keyboard = keyboard
        self.cells = []

        self.clickSwitch = False

    def updatePlayground(self):
        if(self.keyboard.spaceKey):
            self.updateCells()
        self.mouseInput()

    def mouseInput(self):
        xPos = self.mouse.xGridPos
        yPos = self.mouse.yGridPos

        if(self.mouse.leftButton and self.clickSwitch == False):
            if(self.keyboard.shiftKey):
                clickedCell = self.checkIfCellExist(xPos, yPos)
                if(clickedCell == False):
                    self.createCell(xPos, yPos)
                else:
                    self.deleteCell(clickedCell)
            self.clickSwitch = True

        if (self.mouse.leftButton == False and self.clickSwitch == True):

            self.clickSwitch = False

    def deleteCell(self, cell):
        index = self.cells.index(cell)
        self.cells[index].delete()
        self.cells.remove(cell)

    def createCell(self, xPos, yPos):
        self.cells.append(Cell(self.screen, xPos, yPos))

    def checkIfCellExist(self, xPos, yPos):
        for cell in self.cells:
            if(xPos == cell.x and yPos == cell.y):
                return cell
        return False

    def getNeighborAmount(self, coord):
        sum = 0
        xPos = coord[0][0]
        yPos = coord[0][1]
        for indexX in range(xPos - 1, xPos + 2):
            for indexY in range(yPos - 1, yPos + 2):
                if(xPos == indexX and yPos == indexY): 
                    continue
                if(coord[xPos]):
                    sum += 1

        return sum

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
                        cellToCheck = self.checkIfCellExist(indexX, indexY)
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
