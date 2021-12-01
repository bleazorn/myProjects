from tkinter import *
import tkinter as tk
from tkinter import ttk, colorchooser

from GUI.frameSuper import FrameSuper


class CategoryFrame(FrameSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(loc)

        # Class attributes
        self.background = background
        self.parent = parent

        # Creation of Widgets
        self.listbox = tk.Listbox(parent, selectmode="extended", exportselection=0)

        self.addCatText = StringVar()
        self.textAddCat = ttk.Entry(parent, textvariable=self.addCatText)
        self.buttAddCat = ttk.Button(parent, text="Add", command=self.addCat)
        self.buttDelCat = ttk.Button(parent, text="Del", command=self.delCat)

        # Grid placement
        self.textAddCat.grid(row=self.row, column=self.col)
        self.buttAddCat.grid(row=self.row, column=self.col+1)
        self.buttDelCat.grid(row=self.row+1, column=self.col+1)
        self.listbox.grid(row=self.row + 2, column=self.col, columnspan=2)

        self.generateListbox()

    # gets a list of names of categories
    def getCatFromData(self):
        ret = []
        for tup in self.background.getCategories():
            ret.append(tup[0])
        return ret

    # creates the listbox of categories
    def generateListbox(self):
        i = 0
        for tup in self.background.getCategories():
            self.addListbox(tup, i)
            i += 1

    # adds a listbox, only do when data is already correct
    def addListbox(self, tup, index):
        self.listbox.insert(index, tup[0])
        self.listbox.itemconfig(index, bg=tup[1])

    # deletes listbox, only do when data is already removed
    def deleteListbox(self, index):
        self.listbox.delete(index, index)

    # adds a category, both listbox and data is updated
    def addCat(self):
        if self.textAddCat.get():
            text = self.textAddCat.get()
            coloring = colorchooser.askcolor(title="Choose color")[1]
            cat = (text, coloring)
            self.addListbox(cat, len(self.background.getCategories()))
            self.background.addCategory(cat)

    # deletes a category, both listbox and data is updated
    def delCat(self):
        selected = self.listbox.curselection()
        for sel in reversed(selected):
            self.deleteListbox(sel)
            self.background.delCategory(sel)
            self.parent.master.event_generate("<<RefreshGraph>>")
            self.parent.master.event_generate("<<RefreshBank>>")

    # moves category to new index, both listbox and data is updated
    def moveCat(self, fromIndex, toIndex):
        lenCat = len(self.background.getCategories())
        if fromIndex < 0 or fromIndex >= lenCat:
            print("given index is not in data")
            return
        if toIndex < 0:
            toIndex = 0
        if toIndex >= lenCat:
            toIndex = lenCat-1

        self.deleteListbox(fromIndex)
        self.addListbox(self.background.getCategories()[toIndex], toIndex)
        self.background.dataMove(fromIndex, toIndex, 1)

    # moves every selected category one up
    def upCat(self, event):
        selected = self.listbox.curselection()
        if len(selected) > 0:
            i = -1
            for sel in selected:
                i += 1
                if sel == i:
                    continue
                self.moveCat(sel, sel - 1)
                self.listbox.select_set(sel-1)
                self.listbox.see(sel-1)

    # moves every selected category one down
    def downCat(self, event):
        selected = self.listbox.curselection()
        if len(selected) > 0:
            for sel in reversed(selected):
                if sel >= len(self.background.getCategories()) or selected.__contains__(sel):
                    continue
                self.moveCat(sel, sel+1)
                self.listbox.select_set(sel+1)
                self.listbox.see(sel+1)

    # change Color
    def changeColor(self, event):
        selected = self.listbox.curselection()
        coloring = colorchooser.askcolor(title="Choose color")
        for sel in selected:
            self.listbox.itemconfig(sel, bg=coloring[1])

    # returns the indexes of the selected categories
    def getSelected(self):
        return self.listbox.curselection()


def test():
    root = Tk()
    frm = ttk.Frame(root)
    frm.grid()
    cats = CategoryFrame(frm, None)

    root.bind('a', cats.delCat)

    root.mainloop()

