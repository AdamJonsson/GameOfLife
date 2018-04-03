from cell import Cell
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox

class UserInterface:

    """
        The inferface for the user. The user can start diffrent moded, 
        import or export the playground to a choosen file, clear the playground, ect.

        Attributes: 
        width: The width of the UI in px
        backgroundColor: The background color of the UI
        headerColor: The header color of the UI
        wecomeFrameActive: If the welcome frame is showing or not
    """

    def __init__(self, root, screen, playground, mouse, keyboard, width):
        self.root = root
        self.screen = screen
        self.playground = playground
        self.mouse = mouse
        self.keyboard = keyboard
        
        self.width = width
        self.backgroundColor = "#DDDDDD" 
        self.headerColor = "#0077CC"

        self.welcomeFrameActive = True

        self.autogenerateButton = Button
        self.clearPalygroundButton = Button
        self.savePlaygroundButton = Button
        self.generateButton = Button

        self.generateAmountEntry = Entry

        self.numberOfCellLabel = Label
        self.numberOfGenerationLabel = Label

        self.createUI()
        self.createWelcomeFrame()

        self.updateLabelTexts()


    def createUI(self):

        """
            Creates the UI.
            :return: (nothing)
        """

        #Main frames
        self.UIFrame = Frame(self.root, width=self.width, height=self.screen.height, bg=self.backgroundColor)
        self.buttonUIFrame = Frame(self.UIFrame)
        self.buttonUIFrame.pack(side="bottom", pady=15, padx=15)
        self.topUIFrame = Frame(self.UIFrame, height=1)
        self.topUIFrame.pack(side="top", pady=15, padx=15, fill=X)

        # Autogenerate button
        self.autogenerateButton = Button(self.buttonUIFrame, width=17, text="Autogenerate", highlightbackground=self.backgroundColor, command=self.autogenerateAction)
        self.autogenerateButton.pack()

        #Generate button
        generationFrame = Frame(self.buttonUIFrame, bg=self.backgroundColor)
        generationFrame.pack(fill=X)

        self.generateAmountEntry = Entry(generationFrame, width=4, highlightbackground=self.backgroundColor)
        self.generateAmountEntry.pack(side=LEFT)
        self.generateButton = Button(generationFrame, text="Generate", highlightbackground=self.backgroundColor, command=self.generateGivenAmount)
        self.generateButton.pack(fill=X)

        #import/export palyground buttons
        importExportFrame = Frame(self.buttonUIFrame, bg=self.backgroundColor)
        importExportFrame.pack(fill=X)

        self.savePlaygroundButton = Button(importExportFrame, text="Export", highlightbackground=self.backgroundColor, command=self.savePlayground)
        self.savePlaygroundButton.pack(side=LEFT, fill=X)
        self.importPlayground = Button(importExportFrame, text="Import", highlightbackground=self.backgroundColor, command=self.loadPlayground)
        self.importPlayground.pack(fill=X)

        #Clear palyground button
        self.clearPalygroundButton = Button(self.buttonUIFrame, text="Clear playground", highlightbackground=self.backgroundColor, command=self.playground.clearPlayground)
        self.clearPalygroundButton.pack(fill=X)

        #Toggle frame button
        self.clearPalygroundButton = Button(self.buttonUIFrame, text="Help", highlightbackground=self.backgroundColor, command=self.toggleFrame)
        self.clearPalygroundButton.pack(fill=X)

        #The program status.
        self.setBlueLabel("Number of cells")
        self.numberOfCellLabel = Label(self.topUIFrame)
        self.numberOfCellLabel.pack(fill=X, padx=5, pady=5)

        self.setBlueLabel("Current generation")
        self.numberOfGenerationLabel = Label(self.topUIFrame)
        self.numberOfGenerationLabel.pack(fill=X, padx=5, pady=5)

        self.setBlueLabel("Last generation time")
        self.generationPerSecoundLabel = Label(self.topUIFrame)
        self.generationPerSecoundLabel.pack(fill=X, padx=5, pady=5)


    def createWelcomeFrame(self):
        """
            Creates the welcome screen, with tutorial screen.
            :return: (nothing)
        """

        self.welcomeFrame = Frame(self.root, width=self.width, height=self.screen.height, bg=self.backgroundColor)
        self.welcomeFrame.pack(side=RIGHT, fill=Y)
        self.buttonWelcomeFrame = Frame(self.welcomeFrame)
        self.buttonWelcomeFrame.pack(side="bottom", pady=15, padx=15)
        self.topWelcomeFrame = Frame(self.welcomeFrame, height=1)
        self.topWelcomeFrame.pack(side="top", pady=15, padx=15, fill=X)

        self.toControllPanelButton = Button(self.buttonWelcomeFrame, width=17, text="Control Panel", highlightbackground=self.backgroundColor, command=self.toggleFrame)
        self.toControllPanelButton.pack()

        #intructionText = "Mouse + hold:\nLook around\n\nMouse + shift + click:\nPlace cell\n\n(+), (-):\nZoom the playground"
        intructionText = "Welcome to Game Of Life!\n\nMouse + Hold: Moving around the playground.\n\nMouse + Shift + Click: Add / Delete a cell in the playground\n\n(+), (-): Zooming\n\nArrow keys: Moving around\n\n\nA cell is born if it has exactly three neighbors. Neighbors are counted horizontally, vertically or diagonally.\n\nA cell dies if it has fewer than two neighbors or if it has more than three neighbors."
        intructionLabel = Label(self.topWelcomeFrame, text=intructionText, anchor='w', justify=LEFT, bg=self.backgroundColor, wrap=175)
        intructionLabel.pack(fill=X)


    def toggleFrame(self):
        """
            Toggle between the welcome screen and the control panel.
            :return: (nothing)
        """
        if(self.welcomeFrameActive):
            self.welcomeFrame.pack_forget()
            self.UIFrame.pack(side=RIGHT, fill=Y)
            self.welcomeFrameActive = False
        else:
            self.UIFrame.pack_forget()
            self.welcomeFrame.pack(side=RIGHT, fill=Y)
            self.welcomeFrameActive = True


    def updateLabelTexts(self):
        """
            Toggle between the welcome screen and the control panel.
            :return: (nothing)
        """
        self.numberOfCellLabel["text"] = str(len(self.playground.cells))
        self.numberOfGenerationLabel["text"] = str(self.playground.generation)
        self.generationPerSecoundLabel["text"] = str(self.playground.timeToCalcGeneration/100) + " ms"

        self.root.after(50, self.updateLabelTexts)
        

    def generateGivenAmount(self):
        """
            Generate the palyground (amount) times.
            :return: (nothing)
        """

        try:
            amountOfGenerations = int(self.generateAmountEntry.get())
        except ValueError:
            messagebox.showerror("Error: Input", "The input you gave must by a number!")
            return

        if(amountOfGenerations > 1000):
            messagebox.showerror("Error: Input", "You can max do 1000 generation per click!")
            return

        for i in range(amountOfGenerations):
            self.playground.nextGeneration()


    def autogenerateAction(self):
        """
            Toggle if the playground should autogenerate or not.
            :return: (nothing)
        """
        if(self.playground.autoGenerateMode == True):
            self.playground.autoGenerateMode = False
            self.autogenerateButton["text"] = "Autogenerate"
        else:
            self.playground.autoGenerateMode = True
            self.autogenerateButton["text"] = "Stop"


    def setBlueLabel(self, text):
        """ 
            Creates a nice label for playground data. 
        """
        newLabel = Label(self.topUIFrame, anchor="w", justify="left", text=text, bg=self.headerColor, fg="white"); newLabel.pack(fill=X)
        return newLabel
        

    def loadPlayground(self):
        """
            The user can choose a file to load.
            :return: (nothing)
        """
        filePath = askopenfilename(initialdir = "Playgrounds",title = "Select file", filetypes = (("Text files","*.txt"), ("all files","*.*")))
        if(filePath != ""):
            self.playground.importPlayground(filePath)


    def savePlayground(self):
        """
            Saving the playground to a choosen file.
            :return: (nothing)
        """
        fileName = "GameOfLife_" + str(self.playground.generation)
        filePath = self.saveBox("Save playground", fileName, "Playgrounds")
        if(filePath != ""):
            self.playground.exportPlayground(filePath)


    def saveBox(self, title=None, fileName=None, dirName=None, fileExt=".txt", fileTypes=None, asFile=False):
        """
            Opens an savefile explorer. 
        """

        if fileTypes is None:
            fileTypes = [('all files', '.*'), ('text files', '.txt')]

        options = {}
        options['defaultextension'] = fileExt
        options['filetypes'] = fileTypes
        options['initialdir'] = dirName
        options['initialfile'] = fileName
        options['title'] = title

        if asFile:
            return asksaveasfile(mode='w', **options)
        else:
            return asksaveasfilename(**options)