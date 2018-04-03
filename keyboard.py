class Keyboard:

    def __init__(self, root):
        self.subtractKey = False
        self.addKey = False
        self.upKey = False
        self.downKey = False
        self.leftKey = False
        self.rightKey = False
        self.escapeKey = False
        self.spaceKey = False
        self.shiftKey = False

        self.root = root

        self.root.bind('<KeyPress>', self.__activateKey)
        self.root.bind('<KeyRelease>', self.__inactivateKey)

        self.keyBindings = {}

    def __activateKey(self, event):
        self.__changeKeyStatus(event, True)
        self.__checkForShortCommands()

    def __inactivateKey(self, event):
        self.__changeKeyStatus(event, False)
        self.__checkForShortCommands()

    def __changeKeyStatus(self, event, mode):


        if(event.keysym in self.keyBindings and mode):
            self.keyBindings[event.keysym]()

        if(event.keysym == "minus"):
            self.subtractKey = mode
        elif(event.keysym == "plus"):
            self.addKey = mode

        if(event.keysym == "Up"):
            self.upKey = mode
        if(event.keysym == "Down"):
            self.downKey = mode
        if(event.keysym == "Left"):
            self.leftKey = mode
        if(event.keysym == "Right"):
            self.rightKey = mode

        if(event.keysym == "Escape"):
            self.escapeKey = mode
        if(event.keysym == "space"):
            self.spaceKey = mode

        if(event.keycode == 131074):
            self.shiftKey = mode
        if(event.keycode == 10616834 or event.keycode == 131330):
            self.shiftKey = True

    def __checkForShortCommands(self):
        if(self.escapeKey):
            self.root.quit()

    def bindFunctionToKey(self, keyname, function):
        self.keyBindings[keyname] = function