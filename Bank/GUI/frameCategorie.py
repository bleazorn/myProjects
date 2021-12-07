from tkinter import *
import tkinter as tk
from tkinter import ttk, colorchooser

from GUI.frameSuper import FrameSuper
from objects.dataCategory import DataCategory


class CategoryFrame(FrameSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

        # Creation of Widgets
        self.listbox = tk.Listbox(parent, selectmode="extended", exportselection=0)

        self.addCatText = StringVar()
        self.textAddCat = ttk.Entry(parent, textvariable=self.addCatText)
        self.buttAddCat = ttk.Button(parent, text="Add", command=self.addCat)
        self.buttDelCat = ttk.Button(parent, text="Del", command=self.delCat)
        self.buttBacCat = ttk.Button(parent, text="Back", command=self.backSubCat)

        # Grid placement
        self.textAddCat.grid(row=self.row, column=self.col)
        self.buttAddCat.grid(row=self.row, column=self.col+1)
        self.buttBacCat.grid(row=self.row+1, column=self.col)
        self.buttDelCat.grid(row=self.row+1, column=self.col+1)
        self.listbox.grid(row=self.row + 2, column=self.col, columnspan=2)

        self.listbox.bind('<Double-Button-1>', self.getSubCat)

        self.generateListbox()

    # gets a list of names of categories
    def getCatFromData(self):
        ret = []
        for cat in self.background.getCategoriesForGui():
            if not isinstance(cat, DataCategory):
                return
            ret.append(cat.getName())
        return ret

    # creates the listbox of categories
    def generateListbox(self):
        self.listbox.delete(0, self.listbox.size())
        i = 0
        for cat in self.background.getCategoriesForGui():
            self.addListbox(cat, i)
            i += 1

    def generateNewEvent(self, event):
        self.generateListbox()

    # adds a listbox, only do when data is already correct
    def addListbox(self, cat, index):
        if not isinstance(cat, DataCategory):
            return
        self.listbox.insert(index, cat.getName())
        self.listbox.itemconfig(index, bg=cat.getColor())

    # deletes listbox, only do when data is already removed
    def deleteListbox(self, index):
        self.listbox.delete(index, index)

    # adds a category, both listbox and data is updated
    def addCat(self):
        if self.textAddCat.get():
            text = self.textAddCat.get()
            coloring = colorchooser.askcolor(title="Choose color")[1]
            cat = DataCategory(text, coloring)
            self.background.addCategory(cat)
            self.addListbox(cat, self.listbox.size())

    # deletes a category, both listbox and data is updated
    def delCat(self):
        selected = self.listbox.curselection()
        for sel in reversed(selected):
            self.background.delCategory(sel)
            self.deleteListbox(sel)
            self.parent.master.event_generate("<<RefreshGraph>>")
            self.parent.master.event_generate("<<RefreshBank>>")

    # moves category to new index, both listbox and data is updated
    def moveCat(self, fromIndex, toIndex):
        lenCat = len(self.background.getCategoriesForGui())
        if fromIndex < 0 or fromIndex >= lenCat:
            print("given index is not in data")
            return
        if toIndex < 0:
            toIndex = 0
        if toIndex >= lenCat:
            toIndex = lenCat-1

        self.deleteListbox(fromIndex)
        self.background.dataMove(fromIndex, toIndex, 1)
        self.addListbox(self.background.getCategoriesForGui()[toIndex], toIndex)

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
                if sel >= len(self.background.getCategoriesForGui()) or selected.__contains__(sel):
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

    # get the sub categories from selected categorie
    def getSubCat(self, event):
        selected = self.getSelected()
        if selected:
            self.background.getSubCategories(selected[0])
            self.generateListbox()
            self.parent.master.event_generate("<<RefreshGraph>>")

    # goes back to the upper subcategory
    def backSubCat(self):
        self.background.goParentSubCat()
        self.generateListbox()
        self.parent.master.event_generate("<<RefreshGraph>>")


def test():
    root = Tk()
    frm = ttk.Frame(root)
    frm.grid()
    cats = CategoryFrame(frm, None)

    root.bind('a', cats.delCat)

    root.mainloop()

