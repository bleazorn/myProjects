from tkinter import *
import tkinter as tk
from tkinter import ttk, colorchooser

from GUI.frameGraph import GraphSuper


class GraphPeriodic(GraphSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

        self.textDate = StringVar()
        self.textEntry = ttk.Entry(parent, textvariable=self.textDate)
        self.periodic = ttk.Entry(parent, textvariable=self.textDate)
        self.buttRefresh = ttk.Button(parent, text="Refresh", command=self.create)

        self.textEntry.grid(row=self.row, column=self.col)
        self.periodic.grid(row=self.row, column=self.col + 1)
        self.buttRefresh.grid(row=self.row, column=self.col + 2)


    def create(self):
        print("yeee")

    def reFresh(self):
        pass
