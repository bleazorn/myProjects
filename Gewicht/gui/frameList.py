from tkinter import *
import tkinter as tk
from tkinter import ttk

from gui.frameSuper import FrameSuper
from objects.weightObj import WeightObj


class ListFrame(FrameSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

        self.listbox = tk.Listbox(parent, selectmode="extended", width=120, height=25, exportselection=0)
        self.listbox.grid(row=self.row, column=self.col, rowspan=2)

        self.generateListbox(background.getData())

    # creates the listbox from the variable data
    def generateListbox(self, data):
        if not data:
            return
        i = 0
        for dat in data:
            self.addListbox(dat, i)
            i += 1

    # generates new listbox
    def generateNew(self, data):
        self.listbox.delete(0, self.listbox.size())
        self.generateListbox(data)

    # adds a listbox, only do when data is already correct
    def addListbox(self, dat, index):
        if type(dat) is WeightObj:
            self.listbox.insert(index, str(dat))
            self.listbox.itemconfig(index, bg=dat.getColor())

    # deletes listbox, only do when data is already removed
    def deleteListbox(self, index):
        self.listbox.delete(index, index)

    # returns the selected items of the  listbox
    def getSelected(self):
        return self.listbox.curselection()
