from tkinter import *
import tkinter as tk
from tkinter import ttk, colorchooser

from tkcalendar import DateEntry

from GUI.frameGraph import GraphSuper
from datetime import date
from dateutil.relativedelta import relativedelta


class GraphPeriodic(GraphSuper):
    periods = ["Days", "Weeks", "Months", "Years"]

    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

        self.dateFirst = DateEntry(self.parent, name="first", selectmode='day', date_pattern='dd/MM/yyyy')
        self.dateFirst.set_date(date.today() - relativedelta(years=1))

        self.textDate = StringVar()
        self.textDate.set("1")
        self.textEntry = ttk.Entry(parent, textvariable=self.textDate)
        self.periodic = ttk.Combobox(parent, values=self.periods, state="readonly")
        self.textCount = StringVar()
        self.textCount.set("12")
        self.entryCount = ttk.Entry(parent, textvariable=self.textCount)

        self.buttRGraph.grid(row=self.row + 0, column=self.col + 3)
        self.textEntry.grid(row=self.row + 1, column=self.col + 1)
        self.periodic.grid(row=self.row + 1, column=self.col + 2)
        self.entryCount.grid(row=self.row + 1, column=self.col + 3)
        self.dateFirst.grid(row=self.row + 1, column=self.col + 0)

        self.periodic.current(2)

        self.categories = [0]

        self.textEntry.bind("<Return>", self.periodSelectedEvent)
        self.periodic.bind("<<ComboboxSelected>>", self.periodSelectedEvent)
        self.entryCount.bind("<Return>", self.periodSelectedEvent)

        self.create()

    def create(self):
        c_width = 500
        c_height = 210
        c_marginX = 20
        c_marginYDown = 30
        c_marginYUp = 20

        self.getCategories()
        data = self.getGraphData()

        self.c = Canvas(self.parent, width=c_width, height=c_height)
        self.c.grid(row=self.row + 2, column=self.col, rowspan=2, columnspan=4)

        self.c.create_line(0, c_height - c_marginYDown, c_width, c_height - c_marginYDown)

        try:
            c_barWidth = (c_width - ((len(data) + 1) * c_marginX)) // len(data)
            c_barHeight = c_height - c_marginYDown - c_marginYUp
            c_textHeight = c_height - 13

            maxValue = 0
            for per in data:
                for cat in data[per]:
                    bedrag = abs(data[per][cat])
                    if bedrag > maxValue:
                        maxValue = bedrag

            i = 0
            for per in data:
                j = 0
                catStart = c_marginX + (c_marginX + c_barWidth) * i
                for cat in data[per]:
                    x1 = catStart + j * (c_barWidth//len(data[per]))
                    x2 = x1 + c_barWidth//len(data[per])

                    y1 = int(c_height - (c_marginYDown + (abs(data[per][cat]) / maxValue) * c_barHeight))
                    y2 = c_height - c_marginYDown

                    self.c.create_rectangle(x1, y1, x2, y2, fill=cat[1])
                    self.c.create_text((x1 + x2) // 2, y1 - 5, text=str("{:.2f}".format(data[per][cat])), font=("Purisa", 5))

                    j += 1
                bartext = str(per[0]) + "\n        -\n" + str(per[1])
                self.c.create_text(catStart + (c_barWidth // 2), c_textHeight, text=bartext, font=("Purisa", 5))
                i += 1

        except ZeroDivisionError:
            print("No categories. NNullpointError in Graph")

    def getCategories(self):
        self.getRoot().event_generate("<<periodicCat>>")

    def setCategories(self, categories):
        if not categories:
            categories = [0]
        self.categories = list(categories)

    def getGraphData(self):
        periodV = self.textEntry.get()
        try:
            periodV = int(periodV)
        except (TypeError, ValueError):
            print("put a natural number")
            periodV = 1
            self.textDate.set("1")

        periodD = self.periodic.get()

        rd = relativedelta(months=1)
        if periodD == "Days":
            rd = relativedelta(days=periodV)
        elif periodD == "Weeks":
            rd = relativedelta(weeks=periodV)
        elif periodD == "Months":
            rd = relativedelta(months=periodV)
        elif periodD == "Years":
            rd = relativedelta(years=periodV)

        countV = self.entryCount.get()
        try:
            countV = int(countV)
        except (TypeError, ValueError):
            print("put a natural number")
            countV = 12
            self.textCount.set("12")

        return self.background.getGraphDataPeriodic(self.categories, rd, countV, self.dateFirst.get_date())

    def periodSelectedEvent(self, event):
        self.getRoot().focus_set()
        self.create()

    def destroy(self):
        super().destroy()
        self.c.destroy()
        self.textEntry.destroy()
        self.periodic.destroy()
        self.entryCount.destroy()
        self.dateFirst.destroy()

    def reFresh(self):
        pass
