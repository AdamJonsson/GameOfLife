class Cell:

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
        xPos = self.x * self.screen.gridSize * self.screen.totalZoom + self.screen.topLeftBorderX 
        yPos = self.y * self.screen.gridSize * self.screen.totalZoom + self.screen.topLeftBorderY
        xPosEnd = xPos + self.screen.gridSize * self.screen.totalZoom
        yPosEnd = yPos + self.screen.gridSize * self.screen.totalZoom
        self.rect = self.screen.canvas.create_rectangle(xPos, yPos, xPosEnd, yPosEnd, fill=self.color, outline="")

    def makeAlive(self):
        self.dead = False
        self.createVisualCell()

    def delete(self):
        if(self.rect):
            self.screen.canvas.delete(self.rect)