from objects.weightObj import WeightObj
import reader.csvReader as csvReader

from datetime import date, timedelta


class Background:
    def __init__(self, csvFile):
        self.csvFile = csvFile
        self.data = csvReader.getDataFromCsv(self.csvFile)
        self.data.sort(key=lambda x: x.sortDatum(), reverse=True)
        a = ""

    def getData(self):
        return self.data

    def addWeight(self, element):
        self.data.insert(0, element)
        csvReader.writeRowsToCsv(self.csvFile, self.data)

    def delWeight(self, index):
        self.data.pop(index)
        csvReader.writeRowsToCsv(self.csvFile, self.data)

    def moveWeights(self, fromIndex, toIndex):
        if fromIndex < 0 or fromIndex >= len(self.data):
            print("given index is not in data")
            return
        if toIndex < 0:
            toIndex = 0
        if toIndex >= len(self.data):
            toIndex = len(self.data)-1
        temp = self.data.pop(fromIndex)
        self.data.insert(toIndex, temp)

    def changeMorning(self, index, morning):
        ele = self.data.pop(index)
        ele.setMorning(morning)

        self.data.insert(index, ele)
        csvReader.writeRowsToCsv(self.csvFile, self.data)

    def changeEvening(self, index, evening):
        ele = self.data.pop(index)
        ele.setEvening(evening)

        self.data.insert(index, ele)
        csvReader.writeRowsToCsv(self.csvFile, self.data)

    def changeColor(self, index, coloring):
        ele = self.data.pop(index)
        ele.setColor(coloring)
        
        self.data.insert(index, ele)
        csvReader.writeRowsToCsv(self.csvFile, self.data)

    def updateWeights(self):
        firstDay = self.lastDay()
        lastDay = date.today()

        dates = getDatesBetween(firstDay, lastDay)
        for datum in dates:
            ele = WeightObj(datum)
            self.data.insert(0, ele)
        csvReader.writeRowsToCsv(self.csvFile, self.data)

    def lastDay(self):
        if len(self.data) > 0:
            return self.data[0].getDate()
        else:
            return date.today()


def getDatesBetween(firstDay, lastDay):
    date_modified = firstDay
    ret = []

    while date_modified < lastDay:
        date_modified += timedelta(days=1)
        ret.append(date_modified)

    return ret

