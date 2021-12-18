from tkinter import *
from tkinter import ttk
from GUI.frameGraph import GraphSuper


class GraphStats(GraphSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

        self.create()

    def create(self):
        data = self.background.getGraphDataStats()
        self.getRemaining(data)
        text = self.generateText(data, "")
        self.textLabel = ttk.Label(self.parent, text=text)
        self.textLabel.grid(row=self.row+1, column=self.col)

    def destroy(self):
        self.textLabel.destroy()

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



