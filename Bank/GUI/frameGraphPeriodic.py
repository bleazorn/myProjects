from tkinter import *
import tkinter as tk
from tkinter import ttk, colorchooser

from GUI.frameGraph import GraphSuper


class GraphPeriodic(GraphSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

        periods = ["Days", "Weeks", "Months", "Years"]

        self.textDate = StringVar()
        self.textEntry = ttk.Entry(parent, textvariable=self.textDate)
        self.periodic = ttk.Combobox(parent, values=periods, state="readonly")
        self.buttRefresh = ttk.Button(parent, text="Refresh", command=self.create)

        self.textEntry.grid(row=self.row, column=self.col)
        self.periodic.grid(row=self.row, column=self.col + 1)
        self.buttRefresh.grid(row=self.row, column=self.col + 2)

        self.periodic.current(0)

        self.periodic.bind("<<ComboboxSelected>>", self.periodSelectedEvent)

    def create(self):
        a = self.periodic.get()
        print("yeee " + a)

    def periodSelectedEvent(self, event):
        self.create()

    def reFresh(self):
        pass
