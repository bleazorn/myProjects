from tkinter import *
import tkinter as tk
from tkinter import ttk

from GUI.frameSuper import FrameSuper
from objects.dataBank import DataBank


class BankStatementFrame(FrameSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(loc)

        self.parent = parent
        self.background = background

        self.listbox = tk.Listbox(parent, selectmode="extended", width=120, height=25, exportselection=0)
        #self.listbox.pack(expand=1, fill="both")
        self.listbox.grid(row=self.row, column=self.col, rowspan=3)

        self.generateListbox()

    # creates the listbox from the variable data
    def generateListbox(self):
        data = self.background.getBankStatementsForGui()
        i = 0
        for dat in data:
            self.addListbox(dat, i)
            i += 1

    # generates new listbox
    def generateNew(self):
        self.listbox.delete(0, self.listbox.size())
        self.generateListbox()

    # eventform for generatenew
    def generateNewEvent(self, event):
        self.generateNew()

    # adds a listbox, only do when data is already correct
    def addListbox(self, dat, index):
        if type(dat) is tuple and len(dat) == 2:
            self.listbox.insert(index, dat[0])
            self.listbox.itemconfig(index, bg=dat[1])

    # deletes listbox, only do when data is already removed
    def deleteListbox(self, index):
        self.listbox.delete(index, index)


    # sort listbox on certain data element
    def sortStatements(self, event):
        self.background.sortBankStatements()
        self.generateNew()

    # returns the indexes of selected bankstatements
    def getSelecteds(self):
        return self.listbox.curselection()

    # Colors statement with index
    def colorStatement(self, index, coloring):
        self.listbox.itemconfig(index, bg=coloring)


def test():
    root = Tk()
    frm = ttk.Frame(root)
    frm.grid()
    banF = BankStatementFrame(frm, None)
    root.mainloop()


