from tkinter import *

from tkcalendar import DateEntry
from babel.numbers import *

from GUI.frameGraph import GraphSuper

from datetime import date
from dateutil.relativedelta import relativedelta


class GraphInVsOut(GraphSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)
        self.parent = parent
        self.c = None

        self.dateFirst = DateEntry(self.parent, name="first", selectmode='day', date_pattern='dd/MM/yyyy')
        self.dateLast = DateEntry(self.parent, selectmode='day', name="last",  date_pattern='dd/MM/yyyy')

        self.dateFirst.set_date(date.today() - relativedelta(years=1))
        self.dateLast.set_date(date.today())

        self.dateFirst.grid(row=self.row + 1, column=self.col)
        self.dateLast.grid(row=self.row + 1, column=self.col+2)

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
        self.c.grid(row=self.row + 2, column=self.col, rowspan=2, columnspan=3)

        self.c.create_line(0, c_height - c_marginYDown, c_width, c_height - c_marginYDown)

        try:
            c_barWidth = (c_width - ((2 + 1) * c_marginX)) // 2
            c_barHeight = c_height - c_marginYDown - c_marginYUp
            c_textHeight = c_height - 13

            outcome = []
            income = []
            outcomeVal = 0
            incomeVal = 0
            for tup in data:
                bedrag = tup[1]
                if bedrag < 0:
                    bedrag = - bedrag
                    outcomeVal += bedrag
                    newTup = (tup[0], bedrag, tup[2])
                    outcome.append(newTup)
                elif bedrag >= 0:
                    incomeVal += bedrag
                    income.append(tup)

            maxValue = incomeVal
            if incomeVal < outcomeVal:
                maxValue = outcomeVal

            pixelPerValue = c_barHeight / maxValue  # pixel/bedrag vb. 500/1000=> 500 euro == 250 pixels

            self.createBar(income, pixelPerValue, c_marginX, c_barWidth, c_height, c_marginYDown, c_textHeight, "income\n" + "{:.2f}".format(incomeVal))
            self.createBar(outcome, pixelPerValue, c_marginX * 2 + c_barWidth, c_barWidth, c_height, c_marginYDown, c_textHeight, "outcome\n" + "{:.2f}".format(-outcomeVal))

        except ZeroDivisionError:
            print("No categories. NNullpointError in Graph")

    # creates the bar for both income and outcome
    def createBar(self, data, pixelPerValue, c_minX, c_barWidth, c_height, c_marginYDown, c_textHeight, text):
        vorigeHeight = 0
        for tup in data:
            x1 = c_minX
            x2 = c_minX + c_barWidth

            # TODO: make it correcter niet meer afronden
            barHeight = int(tup[1] * pixelPerValue)
            y1 = c_height - c_marginYDown - barHeight - vorigeHeight
            y2 = c_height - c_marginYDown - vorigeHeight
            vorigeHeight += barHeight

            self.c.create_rectangle(x1, y1, x2, y2, fill=tup[2])
            self.c.create_text((x1 + x2) // 2, c_textHeight, text=text)




def test(event):
    print('date selected')
