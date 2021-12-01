from gui.gui import Gui
from background.background import Background
import os

def getCSVFile():
    dirPath = os.path.dirname(os.path.abspath(__file__))
    dirPath = "D:\Workspace\python\Gewicht"
    return dirPath + "\data\weight.csv"


def getDirOfFile(file):
    return "\\".join(file.split('\\')[:-1])


def main():
    csvFile = getCSVFile()
    if not os.path.exists(getDirOfFile(csvFile)):
        os.mkdir(os.path.dirname(getDirOfFile(csvFile)))
    if not os.path.exists(csvFile):
        f = open(csvFile, 'w', encoding='UTF8')
        f.close()
    background = Background(csvFile)
    Gui(background)


if __name__ == "__main__":
    main()
