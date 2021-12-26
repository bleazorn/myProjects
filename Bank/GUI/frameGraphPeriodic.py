from tkinter import *
import tkinter as tk
from tkinter import ttk, colorchooser

from tkcalendar import DateEntry

from GUI.frameGraph import GraphSuper
from datetime import date
from dateutil.relativedelta import relativedelta


class GraphPeriodic(GraphSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

        periods = ["Days", "Weeks", "Months", "Years"]

        self.dateFirst = DateEntry(self.parent, name="first", selectmode='day', date_pattern='dd/MM/yyyy')
        self.dateLast = DateEntry(self.parent, selectmode='day', name="last",  date_pattern='dd/MM/yyyy')

        self.dateFirst.set_date(date.today() - relativedelta(years=1))
        self.dateLast.set_date(date.today())

        self.textDate = StringVar()
        self.textEntry = ttk.Entry(parent, textvariable=self.textDate)
        self.periodic = ttk.Combobox(parent, values=periods, state="readonly")

        self.buttRGraph.grid(row=self.row, column=self.col + 3)
        self.dateFirst.grid(row=self.row + 1, column=self.col + 0)
        self.textEntry.grid(row=self.row + 1, column=self.col + 1)
        self.periodic.grid(row=self.row + 1, column=self.col + 2)
        self.dateLast.grid(row=self.row + 1, column=self.col + 3)

        self.periodic.current(0)

        self.periodic.bind("<<ComboboxSelected>>", self.periodSelectedEvent)

        self.create()

    def create(self):
        a = self.periodic.get()

        c_width = 500
        c_height = 210
        c_marginX = 20
        c_marginYDown = 30
        c_marginYUp = 20

        first = self.dateFirst.get_date()
        last = self.dateLast.get_date()
        data = self.background.getGraphDataBetweenDates(first, last)

        self.c = Canvas(self.parent, width=c_width, height=c_height)
        self.c.grid(row=self.row + 2, column=self.col, rowspan=2, columnspan=4)

        print("yeee " + a)

    def periodSelectedEvent(self, event):
        self.create()

    def destroy(self):
        super().destroy()
        self.c.destroy()
        self.dateFirst.destroy()
        self.dateLast.destroy()
        self.textEntry.destroy()
        self.periodic.destroy()

    def reFresh(self):
        pass
