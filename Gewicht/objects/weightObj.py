from datetime import date


class WeightObj:
    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) is not list:
            self.datum = self.transformToDate(args[0])
            self.morning = -1
            self.evening = -1
            self.coloring = "white"
        elif len(args) == 1 and type(args[0]) is list:
            self.datum = self.transformToDate(args[0][0])
            self.morning = args[0][1]
            self.evening = args[0][2]
            self.coloring = args[0][3]
        elif len(args) == 4:
            self.datum = self.transformToDate(args[0])
            self.morning = args[1]
            self.evening = args[2]
            self.coloring = args[3]

    def getDate(self):
        return self.datum

    def setDate(self, datum):
        self.datum = datum

    # gives a value that can be used to sort on a date
    def sortDatum(self):
        if isinstance(self.datum, date):
            return self.datum.day + self.datum.month * 100 + self.datum.year * 10000
        return 0

    def transformToDate(self, datum):
        if type(datum) is date:
            return datum
        splt = datum.split('-')
        if len(splt) == 3:
            return date(int(splt[0]), int(splt[1]), int(splt[2]))

    def getMorning(self):
        return self.morning

    def setMorning(self, morning):
        self.morning = morning

    def getEvening(self):
        return self.evening

    def setEvening(self, evening):
        self.evening = evening

    def getColor(self):
        return self.coloring

    def setColor(self, coloring):
        self.coloring = coloring

    def csvRowStr(self):
        return [self.getDate(), self.getMorning(), self.getEvening(), self.getColor()]

    def __repr__(self):
        return str(self.getDate()) + " : " + str(self.getMorning()) + " - " + str(self.getEvening())

    def __str__(self):
        return str(self.getDate()) + " : " + str(self.getMorning()) + " - " + str(self.getEvening())
