class Cell:

    """
        This contains all the data for a cell.

        :param screen: The screen object.
        :param xPos: The x-position for the cell
        :param yPos: The y-position for the cell.
        :param dead: If the cell is dead or not.
        :param color: The color of the cell.

        Attributes: 
        xPos: The x-position on the grid.
        yPos: The y-positoin on the grid.
        color: The color of the cell.
        dead: If the cell is dead.
        numOfNeighbor: The amount of neighbor the cell have.
        rect: An tkinter rect.
    """

    def __init__(self, screen, xPos, yPos, dead=False, color="#ffffff"):

        self.screen = screen
        self.x = xPos
        self.y = yPos
        self.color = color
        self.dead = dead
        self.numOfNeighbor = 0
        self.rect = False

        if(dead == False):
            self.createVisualCell()
    
    def createVisualCell(self):
        """
            Creates an visual rect on the screen.
            :return: (nothing) 
        """
        xPos = self.x * self.screen.gridSize * self.screen.totalZoom + self.screen.topLeftBorderX 
        yPos = self.y * self.screen.gridSize * self.screen.totalZoom + self.screen.topLeftBorderY
        xPosEnd = xPos + self.screen.gridSize * self.screen.totalZoom
        yPosEnd = yPos + self.screen.gridSize * self.screen.totalZoom
        self.rect = self.screen.canvas.create_rectangle(xPos, yPos, xPosEnd, yPosEnd, fill=self.color, outline="")

    def makeAlive(self):
        """
            Make the cell alive insted of dead.
            :return: (nothing)
        """
        self.dead = False
        self.createVisualCell()

    def delete(self):
        """
            Delete the cell by removing the visual part.
            :return: (nothing)
        """
        if(self.rect):
            self.screen.canvas.delete(self.rect)