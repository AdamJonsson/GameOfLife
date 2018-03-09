from tkinter import *
import random
import time

class Playground:
    
    def __init__(self, screen):
        self.cells = []
        self.screen = screen
        pass

    def createRandomCells(self, amount):
        for i in range(amount):
            while True:
                xPos = random.randint(0, 500)
                yPos = random.randint(0, 500)
                if(self.checkIfCellExist(xPos, yPos) == False):
                    break
            self.cells.append(Cell(xPos, yPos, screen))
        
    def checkIfCellExist(self, xPos, yPos):
        for cell in self.cells:
            if(cell.x == xPos and cell.y == yPos): 
                return True
            else:
                return False
        return False


class Cell:

    def __init__(self, x, y, screen, color='#ffffff'):
        self.x = x
        self.y = y
        self.color = color
        self.rect = 0

        self.createRect(screen)

    def createRect(self, screen):
        xPos = self.x * screen.gridSize
        yPos = self.y * screen.gridSize
        self.rect = screen.canvas.create_rectangle(xPos, yPos, xPos + screen.gridSize, yPos + screen.gridSize, fill="#0066ff", outline="")

class Mouse:

    def __init__(self):
        self.mouseButton1 = False
        self.mouseButton2 = False
        self.mouseDragX = 0
        self.mouseDragY = 0
        self.startDragX = 0
        self.startDragY = 0
        self.mouseX = 0
        self.mouseY = 0
        self.zoom = 1
        self.__bindMouseClick()

    def __bindMouseClick(self):
        root.bind("<ButtonPress-1>", self.mouseButton1Down)
        root.bind("<ButtonRelease-1>", self.mouseButton1Up)

    def mouseButton1Down(self, event):
        self.mouseButton1 = True
        self.startDragX = self.mouseX
        self.startDragY = self.mouseY

    def mouseButton1Up(self, event):
        self.mouseButton1 = False
        self.mouseDragX += self.mouseX - self.startDragX
        self.mouseDragY += self.mouseY - self.startDragY

    def getMousePosition(self):
        self.mouseX = root.winfo_pointerx()
        self.mouseY = root.winfo_pointery()


class Screen:
    
    def __init__(self, width, height, canvas, mouse):
        self.canvas = canvas
        self.mouse = mouse
        self.width = width
        self.height = height
        self.offsetX = 0
        self.offsetY = 0
        self.zoom = 0

        self.gridSize = 25
        root.bind("<Key>", self.keyPress)

    def keyPress(self, event):
        if(event.char == "z"): 
            self.zoomScreen(1.1)
        if(event.char == "x"):
            self.zoomScreen(0.9)

    def createGridLines(self):
        gridOffset = 5
        self.vGrid = []
        for i in range(0, int(round(self.width/self.gridSize)) * gridOffset):
            line = self.canvas.create_line(0, self.gridSize * i, self.width * gridOffset, self.gridSize * i, fill="#333366")
            self.vGrid.append(line)

        self.hGrid = []
        for i in range(0, int(round(self.width/self.gridSize)) * gridOffset):
            line = self.canvas.create_line(self.gridSize * i, 0, self.gridSize * i, self.height * gridOffset, fill="#335566")
            self.hGrid.append(line)

    def updateOffset(self):
        mouse.getMousePosition()
        if(mouse.mouseButton1):
            self.offsetX = mouse.mouseX - mouse.startDragX + mouse.mouseDragX
            self.offsetY = mouse.mouseY - mouse.startDragY + mouse.mouseDragY
        else:
            self.offsetX = mouse.mouseDragX
            self.offsetY = mouse.mouseDragY

    def moveScreen(self):
        self.canvas.move(ALL, self.offsetX, self.offsetY)

    def unmoveScreen(self):
        self.canvas.move(ALL, (-1 * self.offsetX), (-1 * self.offsetY))

    def zoomScreen(self, amount):
        self.canvas.scale(ALL, self.width / 2, self.height / 2, amount, amount)


root = Tk()
canvas = Canvas(root, width=700, height=600, bg="black", highlightthickness=0,)
mouse = Mouse()
screen = Screen(700, 600, canvas, mouse)
playground = Playground(screen)

screen.createGridLines()
playground.createRandomCells(10000)

canvas.pack()

while True:
    screen.updateOffset()
    screen.moveScreen()
    canvas.update()
    screen.unmoveScreen()

root.mainloop()
