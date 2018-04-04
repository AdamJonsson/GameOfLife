from tkinter import *
from mouse import Mouse
from keyboard import Keyboard
from screen import Screen
from playground import Playground
from userInterface import UserInterface
import time

#Creating 
root = Tk()
keyboard = Keyboard(root)
mouse = Mouse(root)
screen = Screen(500, 500, mouse, keyboard, root)
playground = Playground(root, screen, mouse, keyboard)
ui = UserInterface(root, screen, playground, mouse, keyboard, 250)

def gameLoop():
    screen.updateScreen()
    playground.updatePlayground()
    root.after(14, gameLoop)

if(__name__ == "__main__"):
    gameLoop()
    root.mainloop()