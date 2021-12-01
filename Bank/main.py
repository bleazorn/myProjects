from GUI.gui import gui
from background.background import Background
import os, sys
import time
from xml.dom import minidom
import traceback
import babel


def getDir():
    application_path = ""
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    # or a script file (e.g. `.py` / `.pyw`)
    elif __file__:
        application_path = os.path.dirname(__file__)
    return application_path + "\\Data"


def createXMLFile(file, rootName):
    root = minidom.Document()

    xml = root.createElement(rootName)
    root.appendChild(xml)

    xml_str = root.toprettyxml(indent="\t")

    with open(file, "w") as f:
        f.write(xml_str)


def main():
    try:
        staFile = getDir() + "\statementXML.xml"
        catFile = getDir() + "\categoryXML.xml"
        if not os.path.exists(os.path.dirname(staFile)):
            os.mkdir(os.path.dirname(staFile))
        if not os.path.exists(staFile):
            createXMLFile(staFile, "metaData")
        if not os.path.exists(catFile):
            createXMLFile(catFile, "metaData")
        background = Background(staFile, catFile)
        gui(background)
    except FileNotFoundError as e:
        print("ERROR: file not found: " + e.filename)


def test():
    csvFile = getDir() + "\csvFile.csv"
    staFile = getDir() + "\statementXML.xml"
    catFile = getDir() + "\categoryXML.xml"
    b = ""

if __name__ == "__main__":
    print("Be patient, program is starting")
    try:
        main()
    except Exception as e:
        print("Sorry an error has occurred. \nTake a screenshot and send it to me")
        traceback.print_exc()
        time.sleep(120)
