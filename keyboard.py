class Keyboard:

    """
        This keeps track on all the keyboard inputs.

        :param root: The root object.

        Attributes: 
            subtractKey: If the key is active or not
            addKey: If the key is active or not
            upKey: If the key is active or not
            downKey: If the key is active or not
            leftKey: If the key is active or not
            rightKey: If the key is active or not
            escapeKey: If the key is active or not
            spaceKey: If the key is active or not
            shiftKey: If the key is active or not
    """

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
        """
            Make an key active
            :param event: The key event
            :return: (nothing)
        """
        self.__changeKeyStatus(event, True)
        self.__checkForShortCommands()

    def __inactivateKey(self, event):
        """
            Make an key inactive
            :param event: The key event
            :return: (nothing)
        """
        self.__changeKeyStatus(event, False)
        self.__checkForShortCommands()

    def __changeKeyStatus(self, event, mode):
        """
            Checks what key to make active/inactive depending on the keysys or keycode.
            :param mode: If the key should be True or False
            :param event: The key event.
            :return: (Nothing)
        """

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

        if(event.keysym == "z"):
            self.shiftKey = mode

    def __checkForShortCommands(self):
        """
            This functions store every short command. 
        """
        if(self.escapeKey):
            self.root.quit()

    def bindFunctionToKey(self, keyname, function):
        """
            Bind an function to an key. If the key is pressed the function is called.
            
            :param keyname: The name of the key.
            :param function: The function to call if the key is pressed.
            :return: (nothing)
        """
        self.keyBindings[keyname] = function