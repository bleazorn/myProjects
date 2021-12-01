from tkinter import *
from tkinter import ttk

from gui.frameGraph import GraphFrame
from gui.frameList import ListFrame


class Gui:
    def __init__(self, background):
        self.background = background

        self.start()

    def start(self):
        root = Tk()
        root.title("Bank checking")

        frm = ttk.Frame(root, padding="3 3 12 12")
        frm.grid(column=0, row=0, sticky=(N, W, E, S))

        self.lisF = ListFrame(frm, self.background, (0, 0))
        self.graF = GraphFrame(frm, None)

        row = 0
        col = 1

        self.addMorText = StringVar()
        self.textAddMor = ttk.Entry(frm, textvariable=self.addMorText)
        self.buttAddMor = ttk.Button(frm, text="Add", command=self.addMor)

        self.addEveText = StringVar()
        self.textAddEve = ttk.Entry(frm, textvariable=self.addEveText)
        self.buttAddEve = ttk.Button(frm, text="Add", command=self.addEve)

        self.buttDates = ttk.Button(frm, text="Update", command=self.updateDates)

        self.textAddMor.grid(row=row, column=col)
        self.buttAddMor.grid(row=row, column=col+1)
        self.textAddEve.grid(row=row+1, column=col)
        self.buttAddEve.grid(row=row+1, column=col+1)
        self.buttDates.grid(row=row + 2, column=col)

        root.mainloop()

    def updateDates(self):
        self.background.updateWeights()
        self.lisF.generateNew(self.background.getData())

    def addMor(self):
        text = self.textAddMor.get()
        self.addMorText.set("")
        selecteds = self.lisF.getSelected()
        if selecteds:
            index = selecteds[0]
            self.background.changeMorning(index, text)
        self.lisF.generateNew(self.background.getData())

    def addEve(self):
        text = self.textAddEve.get()
        self.addEveText.set("")
        selecteds = self.lisF.getSelected()
        if selecteds:
            index = selecteds[0]
            self.background.changeEvening(index, text)
        self.lisF.generateNew(self.background.getData())
