from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog

from GUI.frameBankStatement import BankStatementFrame
from GUI.frameCategorie import CategoryFrame
from GUI.frameGraph import GraphCanvas
from GUI.frameSuper import FrameSuper


class gui:
    def __init__(self, background):
        self.background = background

        root = Tk()

        self.catF = None
        self.banF = None
        self.staF = None

        self.createRoot(root)
        self.createMenu(root)
        self.createFrames(root)
        self.createBindings(root)

        root.mainloop()

    # creates the root of the gui program
    def createRoot(self, root):
        root.title("Bank checking")

        root.tk.call('tk', 'windowingsystem')

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        root.option_add('*tearOff', FALSE)

    # creates the menu of the gui program
    def createMenu(self, parent):
        menubar = tk.Menu(parent)

        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Add File", command=self.addCSVFILE)

        menubar.add_cascade(label="File", menu=filemenu)

        parent.config(menu=menubar)

    # creates the mainframe of the gui program
    def createFrames(self, parent):
        frm = ttk.Frame(parent, padding="3 3 12 12", name="mainFrame")
        frm.grid(column=0, row=0, sticky=(N, W, E, S))

        self.banF = BankStatementFrame(frm, self.background, (0, 0))
        self.catF = CategoryFrame(frm, self.background, (0, 1))
        self.graF = GraphCanvas(frm, self.background.getGraphData(), (0, 3))

        buttColor = ttk.Button(frm, text="Color", command=self.coloring)
        buttColor.grid(row=3, column=0)

        buttColor = ttk.Button(frm, text="Decolor", command=self.decoloring)
        buttColor.grid(row=3+1, column=0)

    # generates all bindings for the root
    def createBindings(self, root):
        root.bind('<<DateEntrySelected>>', self.changeGraph)
        root.bind("<<RefreshGraph>>", self.changeGraph)
        root.bind("<<RefreshBank>>", self.banF.generateNewEvent)

    # adds a csv file
    def addCSVFILE(self):
        csvFile = filedialog.askopenfilename(initialdir="/", title="Open file", filetypes=(("csv files", "*.csv"), ("All files","*.*")))
        self.background.addCSV(csvFile)
        self.banF.generateNew()

    # Colors the selected bankstatemenst with the selected catogrie colors
    def coloring(self):
        if self.frameDoesNotExist(self.catF):
            return

        # list of indexes
        catSel = self.catF.getSelected()
        if catSel:
            colo = self.background.getCategories()[catSel[0]][1]
            self.colorSelected(colo)

    # makes the bankstatements colorless
    def decoloring(self):
        self.colorSelected("white")

    # with selected color, colors the selected bankstatments
    def colorSelected(self, colo):
        if self.frameDoesNotExist(self.banF) or self.frameDoesNotExist(self.graF):
            return

        # number of indexes
        banSel = self.banF.getSelecteds()
        if banSel:
            for sel in banSel:
                self.background.changeColorStatement(sel, colo)
                self.banF.colorStatement(sel, colo)
            self.createGraph()

    # creates the graf including the date entries
    def createGraph(self):
        first = self.graF.dateFirst.get_date()
        last = self.graF.dateLast.get_date()
        a = self.background.getGraphData(first, last)
        self.graF.create(self.background.getGraphData(first, last))

    # event for when one of the date entries have changed
    def changeGraph(self, event):
        self.createGraph()



    @staticmethod
    def frameDoesNotExist(fra):
        return not issubclass(type(fra), FrameSuper)
