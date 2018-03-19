from tkinter import *
import random
import math
import time

class Screen:
    """
        The tkinter window and the canvas. Controlls what is visual on the screen. 

        :param width: The width of the window.
        :param height: The height of the window.
        :param mouse: The mouse object.
        :param keyboard: The keyboard object.
        :param keyboard: The root object.
    """
    
    def __init__(self, width, height, mouse, keyboard, root):
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

        self.setTitle()
        self.createCanvas()
        self.hoverBlock = self.canvas.create_rectangle(0, 0, self.gridSize, self.gridSize, fill="#00ffff")
        self.canvas.bind("<Configure>", self.updateScreenOnResize)
    
    def updateScreenOnResize(self, event):
        """
            Getting the new size of the window screen. Use this only with and configure bind frome tkinter.
        """
        self.height = event.height
        self.width = event.width

    def createCanvas(self):
        """
            Creates a canavs where the playground is going to be renderd on. 
        """
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg="#202020", highlightthickness=0)
        self.canvas.pack(expand=1, side=LEFT, fill=BOTH)
        self.canvas.create_rectangle(0, 0, self.worldSize*self.gridSize, self.worldSize*self.gridSize, fill="black")

    def setTitle(self):
        """
            Setting the window title.
        """
        self.root.title("Game Of LIFE & DEATH!")

    def updateScreen(self):
        """
            Updates the all the objects and input that controlls the screen.
        """
        self.updateMouseInput()
        self.updateKeyboardInput()
        self.updateRealOffset()
        self.checkOffsetBorder()

    def createCanvasGridLines(self):
        """
            Creates grid lines in the canvas. More easy to see the grid system the world is build upon.
        """
        worldSizeInPx = self.gridSize * self.worldSize
        self.vGrid = []
        for i in range(0, self.worldSize + 1):
            color = '#%02x%02x%02x' % (0, 50 - int(i / self.worldSize * 50), int(i / self.worldSize * 100))
            line = self.canvas.create_line(0, self.gridSize * i, worldSizeInPx, self.gridSize * i, fill=color)
            self.vGrid.append(line)

        self.hGrid = []
        for i in range(0, self.worldSize + 1):
            color = '#%02x%02x%02x' % (0, 50 - int(i / self.worldSize * 50), int(i / self.worldSize * 100))
            line = self.canvas.create_line(self.gridSize * i, 0, self.gridSize * i, worldSizeInPx, fill=color)
            self.hGrid.append(line)

    def updateMouseInput(self):
        """
            This method is handeling the input from the user so that the user can move the canvas.
        """

        # Moves the content on the screen
        self.moveCanvasScreen(self.mouse.currentDragAmountX + self.mouse.totalDragAmountX, self.mouse.currentDragAmountY + self.mouse.totalDragAmountY)
    
        # Setting the hover position for the mouse.
        self.updateMouseGridPosition()

        # Having the virutal pointer for the mouse
        hoverX = self.mouse.xGridPos * self.gridSize * self.totalZoom + self.topLeftBorderX
        hoverY = self.mouse.yGridPos * self.gridSize * self.totalZoom + self.topLeftBorderY
        self.canvas.coords(self.hoverBlock, hoverX, hoverY, hoverX + self.gridSize * self.totalZoom, hoverY + self.gridSize * self.totalZoom)


    def updateMouseGridPosition(self):
        """
            This is updating the (grid) position the mouse is hovering over. 
        """
        hoverX = (int((self.mouse.xPos - self.topLeftBorderX) / (self.gridSize * self.totalZoom))) 
        hoverY = (int((self.mouse.yPos - self.topLeftBorderY) / (self.gridSize * self.totalZoom)))
        self.mouse.updateGridPosition(hoverX, hoverY)

    def updateKeyboardInput(self):
        """
            This method is handeling the keyboard input from the user so that the user can move and zoom.
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
            This function is updating the real offset. It is using some objects as refrences where the edge of the world is located. 
        """
        self.topLeftBorderX = self.canvas.coords(self.vGrid[0])[0]
        self.topLeftBorderY = self.canvas.coords(self.vGrid[0])[1]
        self.bottomRightBorderX = self.canvas.coords(self.vGrid[-1])[2]
        self.bottomRightBorderY = self.canvas.coords(self.vGrid[-1])[3]

    def checkOffsetBorder(self):
        """
            Checks if the user is trying to go outside of the playground. If so, this funtion is moving back the player to where to playground is located. 
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
        """
        moveX = xPos - self.offsetX
        moveY = yPos - self.offsetY
        if(abs(moveX) > 0 or abs(moveY) > 0):
            self.canvas.move(ALL, moveX, moveY)
            self.offsetX = xPos
            self.offsetY = yPos

    def changeGridStatus(self, mode):
        """
            Hiding or showing the grid depedning on how much zoom the user is currenlty having. 
        """
        if(mode):
            state = "normal"
        else:
            state = "hidden"
        if(mode != self.gridMode):
            for vGrid in self.vGrid:
                self.canvas.itemconfig(vGrid, state=state)
            for hGrid in self.hGrid:
                self.canvas.itemconfig(hGrid, state=state)
        self.gridMode = mode

    def zoomCanvasScreen(self, amount):
        """
            Zooms the canvas with some amount. 
        """
        if(self.totalZoom * amount < 5 and self.totalZoom * amount > 0.05):
            self.totalZoom *= amount
            if(self.totalZoom < 0.4):
                self.changeGridStatus(False)
            else:
                self.changeGridStatus(True)
            self.canvas.scale(ALL, int(self.width/2), int(self.height/2), amount, amount)

