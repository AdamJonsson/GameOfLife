from cell import Cell
from tkinter import *

class UserInterface:

    def __init__(self, root, screen, playground, mouse, keyboard, width):
        self.root = root
        self.screen = screen
        self.playground = playground
        self.mouse = mouse
        self.keyboard = keyboard
        
        self.width = width

        self.createUI()

    def createUI(self):
        self.UIFrame = Frame(self.root, width=self.width, height=self.screen.height, bg="red")
        self.UIFrame.pack(side=RIGHT, fill=Y)

    