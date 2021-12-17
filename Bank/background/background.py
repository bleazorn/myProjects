import input.csvReader as csvR
import input.categoryReader as catR
import input.statementReader as staR

from datetime import date

from objects.dataBank import DataBank
from objects.dataCategory import DataCategory


class Background:
    def __init__(self, staFileP, catFileP):
        self.staFile = staFileP
        self.catFile = catFileP

        self.dataBan = staR.getBankStatements(self.staFile)

        self.dataCat = catR.getAllCategories(self.catFile)
        self.allCat = self.dataCat
        self.parentCat = ""

        self.automate = False
        self.income = True
        self.sortingOrder = (DataBank.VolgnummerC, False)
        self.sortBankStatements(DataBank.VolgnummerC)

    # returns a list of bankstatements only for background level
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

    # returns a list of bankstatements only for gui level
    def getBankStatementsForGui(self, first=None, last=None):
        ret = []
        ban = self.getBankStatements(first, last)
        for sta in ban:
            ret.append((sta, self.getColorFromStatement(sta)))
        return ret

    # returns the color of the category of the given bankstatement
    def getColorFromStatement(self, statement):
        if not isinstance(statement, DataBank):
            return
        catLoc = statement.getCategoryName()
        if catLoc:
            splt = catLoc.split(".")
            i = len(splt)-1
            temp = self.allCat
            for s in splt:
                for c in temp:
                    if c.getName() == s:
                        if i == 0:
                            return c.getColor()
                        else:
                            temp = c.getSubCategory()
                            i -= 1
                        break
        else:
            return "white"

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
        self.colorIncome()

    # checks if the income category exist, if it does not exist create it
    def checkIfIncomeCategoryExist(self):
        income = DataCategory("Income", "green")
        index = self.getIndexCatWithName(income.getName())
        if index >= 0:
            return index
        else:
            self.addCategory(income)
            return self.getIndexCatWithName(income.getName())

    def getIndexCatWithName(self, name):
        i = 0
        for cat in self.dataCat:
            if cat.getName() == name:
                return i
            i += 1
        return -1

    # goes over every bank statement. If it is positive, it will be classified as income
    def colorIncome(self):
        tempAutomate = self.automate
        self.automate = False

        if not self.income:
            return
        indexCat = self.checkIfIncomeCategoryExist()
        i = 0
        for sta in self.dataBan:
            bedrag = sta.getBedrag()
            if bedrag > 0 and sta.getCategoryName()[:6] != "Income":
                self.changeColorStatement(i, indexCat)
            i += 1

        self.automate = tempAutomate

    # change the color of the bankstatement with the given index
    def changeColorStatement(self, indexSta, indexCat):
        catName = ""
        if indexCat is not None:
            catName = self.dataCat[indexCat].getFullName()
        statement = self.dataBan[indexSta]
        if self.automate:
            staName = statement.getSender()
            for sta in self.dataBan:
                if sta.getSender() == staName:
                    self.changeColorStatementRec(sta, catName)
        else:
            self.changeColorStatementRec(statement, catName)

    # add the categorie to a statement and makes it persistent
    def changeColorStatementRec(self, statement, catName):
        statement.setAttr(DataBank.CategoryNameC, catName)
        staR.changeStatement(self.staFile, statement)

    # sort the bankstatements to the given attribute
    def sortBankStatements(self, attribute):
        reverse = True
        if self.sortingOrder[0] == attribute:
            reverse = not self.sortingOrder[1]
        else:
            if attribute == DataBank.OtherOneC or attribute == DataBank.CategoryNameC:
                reverse = False

        self.dataBan.sort(key=lambda x: x.sort(attribute), reverse=reverse)
        self.sortingOrder = (attribute, reverse)

    # returns a list of categories only for background level
    def getCategories(self):
        return self.dataCat

    # returns a list of categories only for gui level
    def getCategoriesForGui(self):
        return self.getCategories()

    def getColorOfSelectedCategory(self, index):
        return self.dataCat[index].getColor()

    # adds a new category
    # cat is DataCategory type
    def addCategory(self, cat):
        if not isinstance(cat, DataCategory):
            return
        cat.setAttr(DataCategory.parentC, self.parentCat)
        self.dataCat.append(cat)
        catR.addCategory(self.catFile, cat)

    # removes the category at given index
    def delCategory(self, index):
        cat = self.dataCat.pop(index)
        self.decolorStatements(self.parentCat, cat)
        fullName = cat.getName()
        if self.parentCat != "":
            fullName = self.parentCat + "." + fullName
        catR.deleteCategory(self.catFile, fullName)

    # Decolors all statements with the given category
    def decolorStatements(self, parent, cat):
        catName = cat.getName()
        if parent:
            catName = parent + "." + catName
        for sta in self.dataBan:
            if sta.getCategoryName() == catName:
                sta.setAttr(DataBank.CategoryNameC, "")
                staR.changeStatement(self.staFile, sta)
            for sub in cat.getSubCategory():
                self.decolorStatements(catName, sub)

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
    def getGraphDataBetweenDates(self, first=None, last=None):
        stas = self.getBankStatements(first, last)
        cats = self.getCategories()
        ret = []
        temp = {}
        for sta in stas:
            catName = sta.getCategoryName()
            if catName == "":
                continue
            # gets only statemnts under specific parent
            if catName[:len(self.parentCat)] == self.parentCat:
                splt = catName[len(self.parentCat):].split(".")
                if self.parentCat != "":
                    splt = catName[len(self.parentCat) + 1:].split(".")
                if splt:
                    catT = splt[0]
                    if temp.__contains__(catT):
                        temp[catT] = temp[catT] + float(sta.getAttr("Bedrag"))
                    else:
                        temp[catT] = float(sta.getAttr("Bedrag"))
        for cat in cats:
            nameC = cat.getName()
            colorC = cat.getColor()
            if temp.__contains__(nameC):
                count = temp[nameC]
                ret.append((nameC + "\n" + "{:.2f}".format(count), count, colorC))
            else:
                ret.append((nameC, 0, colorC))
        return ret

    def getGraphDataStats(self):
        stas = self.getBankStatements()
        ret = {}
        for sta in stas:
            catName = sta.getCategoryName()
            if catName == "":
                continue

            bedrag = sta.getBedrag()
            parentDic = ret
            for cat in catName.split("."):
                if parentDic.__contains__(cat):
                    temp = parentDic[cat]
                    parentDic[cat] = (temp[0] + bedrag, temp[1])
                else:
                    parentDic[cat] = (bedrag, {})
                parentDic = parentDic[cat][1]

        return ret

    def getGraphDataPeriodic(self, category, periodLenght, periodType, first=None, last=None):
        pass

    # changes the categories to the subcategories of the category with given index
    def getSubCategories(self, index):
        cat = self.dataCat[index]
        if isinstance(cat, DataCategory):
            if self.parentCat:
                self.parentCat += "." + cat.getName()
            else:
                self.parentCat = cat.getName()
            self.dataCat = cat.getSubCategory()

    # Go back to the parent of the current subcategories.
    # if no parent, it stays the same
    def goParentSubCat(self):
        if self.parentCat:
            splt = self.parentCat.split(".")

            temp = self.allCat

            i = len(splt[:-1])
            for s in splt[:-1]:
                for cat in temp:
                    if cat.getName() == s:
                        temp = cat.getSubCategory()
                        i -= 1
                        break

            if i != 0:
                print("Background: can't go up because name was not found")
                return
            self.dataCat = temp
            self.parentCat = ".".join(splt[:-1])


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
