from tkinter import *
from tkinter import ttk
from GUI.frameGraph import GraphSuper


class GraphStats(GraphSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

        self.create()

    def create(self):
        c_width = 500
        c_height = 500
        c_marginX = 20
        c_marginYDown = 30
        c_marginYUp = 20

        data = self.background.getGraphDataStats()
        self.getRemaining(data)

        self.c = Canvas(self.parent, width=c_width, height=c_height)
        self.c.grid(row=self.row + 1, column=self.col, rowspan=3, columnspan=3)

        text = self.generateText(data, "")
        self.c.create_text(100, 200, text=text)

    def destroy(self):
        super().destroy()
        self.c.destroy()

    def generateText(self, data, prefix):
        text = ""
        for cat in data:
            tup = data[cat]
            text += prefix + str(cat) + ":\n"
            text += prefix + "   " + str("{:.2f}".format(tup[0])) + "\n"
            if tup[1]:
                text += self.generateText(tup[1], prefix + "   ")
        return text

    def getRemaining(self, data):
        for cat in data:
            tup = data[cat]
            if tup[1]:
                total = 0
                for subCat in tup[1]:
                    total += tup[1][subCat][0]
                    self.getRemaining(tup[1])
                tup[1]["Remaining"] = (tup[0] - total, {})



