import input.csvReader as csvR
import input.categoryReader as catR
import input.statementReader as staR

from datetime import date

from objects.dataCategory import DataCategory


class Background:
    def __init__(self, staFileP, catFileP):
        self.staFile = staFileP
        self.catFile = catFileP

        self.dataBan = staR.getBankStatements(self.staFile)
        self.dataBan.sort(key=lambda x: x.sortVolgnummer(), reverse=True)

        self.dataCat = catR.getAllCategories(self.catFile)
        self.dataCatT = self.dataCat
        self.parentCat = ""

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

    def getColorOfSelectedCategory(self, index):
        return self.dataCat[index].getColor()

    # adds a new category
    # cat is DataCategory type
    def addCategory(self, cat):
        if not isinstance(cat, DataCategory):
            return
        self.dataCat.append(cat)
        catR.addCategory(self.catFile, cat, self.parentCat)

    # removes the category at given index
    def delCategory(self, index):
        cat = self.dataCat.pop(index)
        self.decolorStatements(cat.getColor())
        catR.deleteCategory(self.catFile, cat.getName())

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
            nameC = cat.getName()
            colorC = cat.getColor()
            if temp.__contains__(colorC):
                ret.append((nameC, -temp[colorC], colorC))
            else:
                ret.append((nameC, 0, colorC))
        return ret

    # changes the categories to the subcategories of the category with given index
    def getSubCategories(self, index):
        cat = self.dataCat[index]
        if isinstance(cat, DataCategory):
            self.parentCat += cat.getName() + "."
            self.dataCat = cat.getSubCategory()

    # Go back to the parent of the current subcategories.
    # if no parent, it stays the same
    def goParentSubCat(self):
        if self.parentCat:
            splt = self.parentCat.split(".")
            if not splt[-1]:
                splt = splt[:-1]

            temp = self.dataCatT

            i = len(splt[:-1])
            for s in splt[:-1]:
                for cat in self.dataCatT:
                    if cat.getName() == s:
                        temp = cat.getSubCategory()
                        i -= 1
                        break

            if i != 0:
                print("Background: can't go up because name was not found")
                return
            self.dataCat = temp
            self.parentCat = ".".join(splt[:-1])
            if self.parentCat:
                self.parentCat += "."

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
