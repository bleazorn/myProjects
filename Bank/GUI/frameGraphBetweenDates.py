from tkinter import *

from tkcalendar import DateEntry
from babel.numbers import *

from GUI.frameGraph import GraphSuper

from datetime import date
from dateutil.relativedelta import relativedelta


class GraphBetweenDates(GraphSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)
        self.parent = parent
        self.c = None

        self.dateFirst = DateEntry(self.parent, name="first", selectmode='day', date_pattern='dd/MM/yyyy')
        self.dateLast = DateEntry(self.parent, selectmode='day', name="last",  date_pattern='dd/MM/yyyy')

        self.dateFirst.set_date(date.today() - relativedelta(years=1))
        self.dateLast.set_date(date.today())

        self.dateFirst.grid(row=self.row, column=self.col)
        self.dateLast.grid(row=self.row, column=self.col+2)

        self.create()

    def create(self):
        c_width = 500
        c_height = 210
        c_marginX = 20
        c_marginYDown = 30
        c_marginYUp = 20

        first = self.dateFirst.get_date()
        last = self.dateLast.get_date()
        data = self.background.getGraphDataBetweenDates(first, last)

        self.c = Canvas(self.parent, width=c_width, height=c_height)
        self.c.grid(row=self.row + 1, column=self.col, rowspan=2, columnspan=3)

        self.c.create_line(0, c_height - c_marginYDown, c_width, c_height - c_marginYDown)

        try:
            c_barWidth = (c_width - ((len(data) + 1) * c_marginX)) // len(data)
            c_barHeight = c_height - c_marginYDown - c_marginYUp
            c_textHeight = c_height - 13

            maxValue = 0
            newData = []
            for tup in data:
                bedrag = abs(tup[1])
                if bedrag > maxValue:
                    maxValue = bedrag
                newData.append((tup[0], bedrag, tup[2]))

            i = 0
            for tup in newData:
                x1 = c_marginX + (c_marginX + c_barWidth) * i
                x2 = (c_marginX + c_barWidth) * (i + 1)
                y1 = int(c_height - (c_marginYUp + (tup[1] / maxValue) * c_barHeight))
                y2 = c_height - c_marginYDown

                self.c.create_rectangle(x1, y1, x2, y2, fill=tup[2])
                self.c.create_text((x1 + x2) // 2, c_textHeight, text=tup[0])
                i += 1

        except ZeroDivisionError:
            print("No categories. NNullpointError in Graph")


def test(event):
    print('date selected')
