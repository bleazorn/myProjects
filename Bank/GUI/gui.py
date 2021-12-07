from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog

from GUI.frameBankStatement import BankStatementFrame
from GUI.frameCategorie import CategoryFrame
from GUI.frameGraphBetweenDates import GraphBetweenDates
from GUI.frameGraphPeriodic import GraphPeriodic
from GUI.frameSuper import FrameSuper
from objects.dataCategory import DataCategory


class gui:
    def __init__(self, background):
        self.background = background

        self.root = Tk()

        self.catF = None
        self.banF = None
        self.staF = None

        self.createRoot(self.root)
        self.createMenu(self.root)
        self.createFrames(self.root)
        self.createBindings(self.root)

        self.root.mainloop()

    # creates the root of the gui program
    def createRoot(self, parent):
        parent.title("Bank checking")

        parent.tk.call('tk', 'windowingsystem')

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        parent.option_add('*tearOff', FALSE)

    # creates the menu of the gui program
    def createMenu(self, parent):
        menuBar = tk.Menu(parent)

        # file menu
        fileMenu = tk.Menu(menuBar)
        fileMenu.add_command(label="Add File", command=self.addCSVFILE)

        menuBar.add_cascade(label="File", menu=fileMenu)

        # settings menu
        settingMenu = tk.Menu(menuBar)
        self.varIncome = IntVar()
        self.varIncome.set(1)
        settingMenu.add_checkbutton(label="Income Check", variable=self.varIncome, command=self.setIncome)
        settingMenu.add_command(label="Income Automate", command=self.autmateIncome)

        menuBar.add_cascade(label="Settings", menu=settingMenu)

        parent.config(menu=menuBar)

    # creates the mainframe of the gui program
    def createFrames(self, parent):
        frm = ttk.Frame(parent, padding="3 3 12 12", name="mainFrame")
        frm.grid(column=0, row=0)

        self.banF = BankStatementFrame(frm, self.background, (0, 0))
        self.catF = CategoryFrame(frm, self.background, (0, 2))
        self.graF = GraphBetweenDates(frm, self.background, (1, 4))

        buttLGraph = ttk.Button(frm, text="<-", command=self.goPreviousGraph)
        buttLGraph.grid(row=0, column=4)

        buttRGraph = ttk.Button(frm, text="->", command=self.goNextGraph)
        buttRGraph.grid(row=0, column=4 + 2)

    # generates all bindings for the root
    def createBindings(self, root):
        root.bind('<<DateEntrySelected>>', self.changeGraph)
        root.bind("<<RefreshGraph>>", self.changeGraph)
        root.bind("<<RefreshBank>>", self.banF.generateNewEvent)
        root.bind("<<RefreshCat>>", self.catF.generateNewEvent)
        root.bind("<<Color>>", self.coloring)
        root.bind("<<Decolor>>", self.decoloring)
        root.bind("<Return>", self.keyEventEnter)
        root.bind("<Delete>", self.keyEventDelete)

    # adds a csv file
    def addCSVFILE(self):
        csvFile = filedialog.askopenfilename(initialdir="/", title="Open file", filetypes=(("csv files", "*.csv"), ("All files","*.*")))
        self.background.addCSV(csvFile)
        self.root.event_generate("<<RefreshBank>>")
        self.root.event_generate("<<RefreshCat>>")
        self.root.event_generate("<<RefreshGraph>>")

    # Colors the selected bankstatemenst with the selected catogrie colors
    def coloring(self, event):
        if self.frameDoesNotExist(self.catF):
            return

        # list of indexes
        catSel = self.catF.getSelected()
        if catSel:
            self.colorSelected(catSel[0])
        self.root.event_generate("<<RefreshBank>>")

    # makes the bankstatements colorless
    def decoloring(self, event):
        self.colorSelected(None)
        self.root.event_generate("<<RefreshBank>>")

    # with selected color, colors the selected bankstatments
    def colorSelected(self, catSel):
        if self.frameDoesNotExist(self.banF) or self.frameDoesNotExist(self.graF):
            return
        colo = "white"
        if catSel is not None:
            colo = self.background.getColorOfSelectedCategory(catSel)
        # number of indexes
        banSel = self.banF.getSelecteds()
        if banSel:
            for sel in banSel:
                self.background.changeColorStatement(sel, catSel)
                self.banF.colorStatement(sel, colo)
            self.createGraph()

    # recreates the graf
    def createGraph(self):
        self.graF.create()

    # event for when one of the date entries have changed
    def changeGraph(self, event):
        self.createGraph()

    # What to do when pressed enter
    def keyEventEnter(self, event):
        if self.frameDoesNotExist(self.catF):
            return
        if self.catF.textAddCat.get():
            self.catF.addCat()

    # What to do when pressed delete
    def keyEventDelete(self, event):
        if self.frameDoesNotExist(self.catF):
            return
        sel = self.catF.getSelected()
        if sel:
            self.catF.delCat()

    def setIncome(self):
        if self.varIncome.get():
            self.background.income = True
        else:
            self.background.income = False

    def autmateIncome(self):
        self.background.colorIncome()
        self.root.event_generate("<<RefreshBank>>")

    # go to the next graph type
    def goNextGraph(self):
        pass

    # go to the previous graph type
    def goPreviousGraph(self):
        pass

    # changes the graph type
    def newGraph(self, index):
        pass

    @staticmethod
    def frameDoesNotExist(fra):
        return not isinstance(fra, FrameSuper)
