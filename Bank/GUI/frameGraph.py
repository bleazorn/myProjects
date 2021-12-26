from tkinter import *
from tkinter import ttk

from tkcalendar import DateEntry
from babel.numbers import *
from GUI.frameSuper import FrameSuper

from datetime import date
from dateutil.relativedelta import relativedelta


class GraphSuper(FrameSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)
        self.buttLGraph = ttk.Button(parent, text="<-", command=self.goPreviousGraph)
        self.buttLGraph.grid(row=self.row, column=self.col)

        self.buttRGraph = ttk.Button(parent, text="->", command=self.goNextGraph)
        self.buttRGraph.grid(row=self.row, column=self.col + 2)

    def create(self):
        pass

    def destroy(self):
        self.buttLGraph.destroy()
        self.buttRGraph.destroy()

    def goPreviousGraph(self):
        self.getRoot().event_generate("<<PrevGraph>>")
        self.destroy()

    def goNextGraph(self):
        self.getRoot().event_generate("<<NextGraph>>")
        self.destroy()


