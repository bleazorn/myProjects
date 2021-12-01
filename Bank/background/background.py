import input.csvReader as csvR
import input.categoryReader as catR
import input.statementReader as staR

from datetime import date


class Background:
    def __init__(self, staFileP, catFileP):
        self.staFile = staFileP
        self.catFile = catFileP

        self.dataBan = staR.getBankStatements(self.staFile)
        self.dataBan.sort(key=lambda x: x.sortVolgnummer(), reverse=True)

        self.dataCat = catR.getCategories(self.catFile)

    # returns a list of bankstatemnts
    def getBankStatements(self, first=None, last=None):
        if first and last:
            ret = []
            for dat in self.dataBan:
                datum = dat.getAttr("Uitvoeringsdatum")
                datumDate = self.changeDatumStrInDate(datum)
                if datumDate:
                    if first <= datumDate <= last:
                        ret.append(dat)
            return ret
        return self.dataBan

    # add a csvfile to the data xml file and sees there are no duplicates
    def addCSV(self, csvFile):
        # TODO: better check so that missing middle statments are also added
        self.dataBan.sort(key=lambda x: x.sortVolgnummer(), reverse=True)
        stats = csvR.readCSVFile(csvFile)
        for sta in stats:
            if len(self.dataBan) > 0:
                if sta.getAttr("Volgnummer") == self.dataBan[0].getAttr("Volgnummer"):
                    break
            staR.addStatement(self.staFile, sta)

        self.dataBan = staR.getBankStatements(self.staFile)
        self.dataBan.sort(key=lambda x: x.sortVolgnummer(), reverse=True)

    # generates an xml file from a csv file
    def __generateXMLFromCSV(self, csvFile):
        stats = csvR.readCSVFile(csvFile)
        for sta in stats:
            staR.addStatement(self.staFile, sta)

    # change the color of the bankstament wiht the given index
    def changeColorStatement(self, index, colo):
        statement = self.dataBan[index]
        statement.setAttr("Color", colo)
        staR.changeStatement(self.staFile, statement)

    # returns a list of categories
    def getCategories(self):
        return self.dataCat

    # adds a new category
    # cat = (name, color)
    def addCategory(self, cat):
        self.dataCat.append(cat)
        catR.addCategory(self.catFile, cat, None)

    # removes the category at given index
    def delCategory(self, index):
        cat = self.dataCat.pop(index)
        self.decolorStatements(cat[1])
        catR.deleteCategory(self.catFile, cat[0])

    # Decolors all statements with the given coloring
    def decolorStatements(self, coloring):
        for sta in self.dataBan:
            if sta.getAttr("Color") == coloring:
                sta.setAttr("Color", "White")
                staR.changeStatement(self.staFile, sta)

    # moves data from one index to another, only do when you also move listbox
    # 0 for bankstatements, 1 for categorie
    def dataMove(self, fromIndex, toIndex, which):
        data = []
        if which == 0:
            data = self.dataBan
        elif which == 1:
            data = self.dataCat

        if fromIndex < 0 or fromIndex >= len(data):
            print("given index is not in data")
            return
        if toIndex < 0:
            toIndex = 0
        if toIndex >= len(data):
            toIndex = len(data)-1
        temp = data.pop(fromIndex)
        data.insert(toIndex, temp)


    # gets the data for the graph
    def getGraphData(self, first=None, last=None):
        stas = self.getBankStatements(first, last)
        cats = self.getCategories()
        ret = []
        temp = {}
        for sta in stas:
            colo = sta.getAttr("Color")
            if temp.__contains__(colo):
                temp[colo] = temp[colo] + float(sta.getAttr("Bedrag"))
            else:
                temp[colo] = float(sta.getAttr("Bedrag"))
        for cat in cats:
            if temp.__contains__(cat[1]):
                ret.append((cat[0], -temp[cat[1]], cat[1]))
            else:
                ret.append((cat[0], 0, cat[1]))
        return ret

    @staticmethod
    def changeDatumStrInDate(datum):
        splt = datum.split('/')
        if len(splt) == 3:
            return date(int(splt[2]), int(splt[1]), int(splt[0]))
        else:
            return None


def test():
    getDir = "D:\Workspace\python\myProjects\Bank\Data\instance"
    csvFile = getDir + "\csvFile.csv"
    staFile = getDir + "\statementXML.xml"
    catFile = getDir + "\categoryXML.xml"
    background = Background(staFile, catFile)
    background.addCSV(csvFile)
