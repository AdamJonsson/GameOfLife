import time

class Mouse:
    """
        This class store all keypresses and the position of the mouse.
        :param root: tkinter object
    """

    def __init__(self, root):
        self.leftButton = False
        self.rightButton = False
        self.xPos = 0
        self.yPos = 0
        self.xGridPos = 0
        self.yGridPos = 0
        self.currentDragAmountX = 0; self.totalDragAmountX = 0; self.startDragAmountX = 0
        self.currentDragAmountY = 0; self.totalDragAmountY = 0; self.startDragAmountY = 0

        self.root = root

        root.bind("<ButtonPress-1>", self.__activateLeftButton)
        root.bind("<ButtonRelease-1>", self.__inactiveLeftButton)

        root.bind("<ButtonPress-2>", self.__activateRightButton)
        root.bind("<ButtonRelease-2>", self.__inactivateRightButton)

        root.bind('<Motion>', self.__getMousePosition)


    def __getMousePosition(self, event):
        """
            Gets the new mouse position.
            :param event: The mouse event.
            :return: (nothing)
        """

        self.xPos = event.x
        self.yPos = event.y
        if(self.leftButton):
            self.updateCurrentDragAmount()

    def __activateLeftButton(self, event):
        """
            Activates the left mouse button and begins to track the drag amount.
            :param event: The mouse button event.
            :return: (nothing)
        """

        self.leftButton = True
        self.startDragAmountX = self.xPos
        self.startDragAmountY = self.yPos

    def __inactiveLeftButton(self, event):
        """
            Inactivates the left mouse button and get the drag amount
            :param event: The mouse button event.
            :return: (nothing)
        """

        self.leftButton = False
        self.saveCurrentDragAmount()

    def __activateRightButton(self, event):
        """
            Activates the right mouse button.
            :param event: The mouse button event.
            :return: (nothing)
        """

        self.rightButton = True

    def __inactivateRightButton(self, event):
        """
            Inactivates the left mouse button.
            :param event: The mouse button event.
            :return: (nothing)
        """

        self.rightButton = False

    def updateCurrentDragAmount(self):
        """
            Kepping track how much the user is draging the mouse.
            :return: (nothing)
        """

        self.currentDragAmountX = self.xPos - self.startDragAmountX
        self.currentDragAmountY = self.yPos - self.startDragAmountY
        
    def saveCurrentDragAmount(self):
        """
            Kepping track how much the user is draging the mouse.
            :return: (nothing)
        """

        self.totalDragAmountX += self.currentDragAmountX
        self.totalDragAmountY += self.currentDragAmountY
        self.currentDragAmountX = 0
        self.currentDragAmountY = 0

    def updateGridPosition(self, xGridPos, yGridPos):
        """
            Updates what grid block the mouse is hovering over.
            :param xGridPos: The grid block in the x-axis
            :param yGridPos: The grid block in the y-axis
            :return: (nothing)
        """

        self.xGridPos = xGridPos
        self.yGridPos = yGridPos
