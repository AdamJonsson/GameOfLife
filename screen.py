from tkinter import *
import random
import math
import time

class Screen:
    """
        The Tkinter window and the canvas. Controlls what is visual on the screen. 

        :param width: The width of the window.
        :param height: The height of the window.
        :param mouse: The mouse object.
        :param keyboard: The keyboard object.
        :param root: The root object.

        Attributes: 
        totalZoom: Keeps track how much zoom the user currently have.
        girdSize: The size of the one grid box in pixels.
        gridMode: Keeps track if the grid is visual or note.
        worldSize: The size of the world.
        offsetX: The canvas offset in the x-axis
        offsetY: The canvas offset in the y-axis
    """
    
    def __init__(self, width, height, mouse, keyboard, root):

        """
            Creating the canvas and other stuff
        """

        self.root = root
        self.keyboard = keyboard
        self.mouse = mouse

        self.width = width
        self.height = height
        self.totalZoom = 1
        self.gridSize = 25 # The value do not really matter for the reason that the user can zoom.'
        self.gridMode = True
        self.worldSize = 200
        self.offsetX = self.worldSize/2 * self.gridSize; self.topLeftBorderX = 0; self.bottomRightBorderX = 0
        self.offsetY = self.worldSize/2 * self.gridSize; self.topLeftBorderY = 0; self.bottomRightBorderY = 0

        self.setTitle("Game Of LIFE & DEATH!")
        self.createCanvas()
        self.hoverBlock = self.canvas.create_rectangle(0, 0, self.gridSize, self.gridSize, fill="#00ff00", outline="")
        self.canvas.bind("<Configure>", self.updateScreenOnResize)

        self.createCanvasGridLines()
    
    def updateScreenOnResize(self, event):
        """
            Getting the new size of the window screen. Use this only with and configure bind from tkinter.
            :return: (nothing)
        """
        self.height = event.height
        self.width = event.width

    def createCanvas(self):
        """
            Creates a canvas where the playground is going to be rendered on. 
            :return: (nothing)
        """
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg="#202020", highlightthickness=0)
        self.canvas.pack(expand=1, side=LEFT, fill=BOTH)
        self.canvas.create_rectangle(0, 0, self.worldSize*self.gridSize, self.worldSize*self.gridSize, fill="black")

    def setTitle(self, title):
        """
            Setting the window title.
            :return: (nothing)
        """
        self.root.title(title)

    def updateScreen(self):
        """
            Updates the all the objects and input that controlls the screen.
            :return: (nothing)
        """
        self.getMouseInput()
        self.getKeyboardInput()
        self.updateRealOffset()
        self.checkOffsetBorder()

        self.canvas.lift(self.hoverBlock)

    def createCanvasGridLines(self):
        """
            Creates grid lines in the canvas. More easy to see the grid system the world is build upon.
            :return: (nothing)
        """
        worldSizeInPx = self.gridSize * self.worldSize
        gridColor = "#202020"
        self.vGrid = []
        for i in range(0, self.worldSize + 1):
            line = self.canvas.create_line(0, self.gridSize * i, worldSizeInPx, self.gridSize * i, fill=gridColor)
            self.vGrid.append(line)

        self.hGrid = []
        for i in range(0, self.worldSize + 1):
            line = self.canvas.create_line(self.gridSize * i, 0, self.gridSize * i, worldSizeInPx, fill=gridColor)
            self.hGrid.append(line)

    def getMouseInput(self):
        """
            This method is handeling the input from the user so that the user can move the canvas.
            :return: (nothing)
        """

        # Moves the content on the screen
        self.moveCanvasScreen(self.mouse.currentDragAmountX + self.mouse.totalDragAmountX, self.mouse.currentDragAmountY + self.mouse.totalDragAmountY)
    
        # Setting the hover position for the mouse.
        self.updateMouseGridPosition()

        # Having the virtual pointer for the mouse
        hoverX = self.mouse.xGridPos * self.gridSize * self.totalZoom + self.topLeftBorderX
        hoverY = self.mouse.yGridPos * self.gridSize * self.totalZoom + self.topLeftBorderY
        self.canvas.coords(self.hoverBlock, hoverX, hoverY, hoverX + self.gridSize * self.totalZoom, hoverY + self.gridSize * self.totalZoom)


    def updateMouseGridPosition(self):
        """
            This is updating the (grid) position the mouse is hovering over. 
            :return: (nothing)
        """
        hoverX = (int((self.mouse.xPos - self.topLeftBorderX) / (self.gridSize * self.totalZoom))) 
        hoverY = (int((self.mouse.yPos - self.topLeftBorderY) / (self.gridSize * self.totalZoom)))
        self.mouse.updateGridPosition(hoverX, hoverY)

    def getKeyboardInput(self):
        """
            This method is handeling the keyboard input from the user so that the user can move and zoom.
            :return: (nothing)
        """

        #Zooming
        if(self.keyboard.addKey):
            self.zoomCanvasScreen(1.02)
        elif(self.keyboard.subtractKey):
            self.zoomCanvasScreen(0.98)

        #Moving
        if(self.keyboard.leftKey):
            self.offsetX -= self.width / 100
        if(self.keyboard.rightKey):
            self.offsetX += self.width / 100
        if(self.keyboard.upKey):
            self.offsetY -= self.width / 100
        if(self.keyboard.downKey):
            self.offsetY += self.width / 100

        #Showing the block cursor.
        if(self.keyboard.shiftKey):
            self.canvas.itemconfig(self.hoverBlock, state="normal")
        else:
            self.canvas.itemconfig(self.hoverBlock, state="hidden")

    def updateRealOffset(self):
        """
            This function is updating the real offset. It is using some objects as reference where the edge of the world is located. 
            :return: (nothing)
        """
        self.topLeftBorderX = self.canvas.coords(self.vGrid[0])[0]
        self.topLeftBorderY = self.canvas.coords(self.vGrid[0])[1]
        self.bottomRightBorderX = self.canvas.coords(self.vGrid[-1])[2]
        self.bottomRightBorderY = self.canvas.coords(self.vGrid[-1])[3]

    def checkOffsetBorder(self):
        """
            Checks if the user is trying to go outside of the playground. If so, this function is moving back the player to where to playground is located. 
            :return: (nothing)
        """
        checkPrecision = 100
        correctionSpeed = 0.20
        if(self.topLeftBorderX > 10/checkPrecision):
            self.offsetX += int(self.topLeftBorderX * correctionSpeed * checkPrecision) / checkPrecision
        if(self.topLeftBorderY > 10/checkPrecision):
            self.offsetY += int(self.topLeftBorderY * correctionSpeed * checkPrecision) / checkPrecision
        
        if(self.bottomRightBorderX - self.width < 10/checkPrecision):
            self.offsetX += int((self.bottomRightBorderX - self.width) * correctionSpeed * checkPrecision) / checkPrecision
        if(self.bottomRightBorderY - self.height < 10/checkPrecision):
            self.offsetY += int((self.bottomRightBorderY - self.height) * correctionSpeed * checkPrecision) / checkPrecision

    def moveCanvasScreen(self, xPos, yPos):
        """
            Moves the screen = Moving all the objects on the canvas. 
            :param xPos: The x-position to move the screen to.
            :param yPos: The y-position to move the screen to.
            :return: (nothing)
        """
        moveX = xPos - self.offsetX
        moveY = yPos - self.offsetY
        if(abs(moveX) > 0 or abs(moveY) > 0):
            self.canvas.move(ALL, moveX, moveY)
            self.offsetX = xPos
            self.offsetY = yPos

    def changeGridStatus(self, stepsBetweenLines):
        """
            Change how many grids there are on the screen.
            :param stepsToShowLine: The amount of steps between lines.
            :return: (nothing)
        """

        i = 0
        for vGrid in self.vGrid:
            i += 1
            if(i % stepsBetweenLines == 0):
                self.canvas.itemconfig(vGrid, state="normal")
            else:
                self.canvas.itemconfig(vGrid, state="hidden")

        i = 0
        for hGrid in self.hGrid:
            i += 1
            if(i % stepsBetweenLines == 0):
                self.canvas.itemconfig(hGrid, state="normal")
            else:
                self.canvas.itemconfig(hGrid, state="hidden")

    def zoomCanvasScreen(self, amount):
        """
            Zooms the canvas with some amount. 
            :param mode: zooms with amount.
            :return: (nothing)
        """
        if(self.totalZoom * amount < 5 and self.totalZoom * amount > 0.05):
            self.totalZoom *= amount

            if(self.totalZoom < 0.1):
                self.changeGridStatus(8)
            elif(self.totalZoom < 0.2):
                self.changeGridStatus(4)
            elif(self.totalZoom < 0.4):
                self.changeGridStatus(2)
            else:
                self.changeGridStatus(1)
            self.canvas.scale(ALL, int(self.width/2), int(self.height/2), amount, amount)

