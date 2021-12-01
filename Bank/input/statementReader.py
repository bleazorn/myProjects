import xml.etree.ElementTree as ET
from objects.dataBank import DataBank


def getBankStatements(dataFile):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()
    ret = []

    for sta in myroot:
        statement = getStatementFromXMLEle(sta)
        ret.append(statement)

    return ret


def getStatementFromXMLEle(sta):
    d = {}
    for child in sta:
        d[child.tag] = child.text
    return DataBank(d)


def addStatement(dataFile, statement, parent=None):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()

    if not parent:
        parent = myroot

    if isinstance(statement, DataBank):
        ele = ET.SubElement(parent, "Statement")

        for att in statement.diction:
            temp = ET.SubElement(ele, att)
            temp.text = statement.getAttr(att)

    mytree.write(dataFile, xml_declaration=True, encoding="UTF-8", method='xml')


def deleteStatement(dataFile, statement):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()

    if isinstance(statement, DataBank):
        for stat in myroot:
            volgNummer = stat.find("Volgnummer").text
            if volgNummer == statement.getAttr("Volgnummer"):
                myroot.remove(stat)
                break

    mytree.write(dataFile, xml_declaration=True, encoding="UTF-8", method='xml')


def changeStatement(dataFile, statement):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()
    if isinstance(statement, DataBank):
        for stat in myroot:
            volgNummer = stat.find("Volgnummer").text
            if volgNummer == statement.getAttr("Volgnummer"):
                d = statement.diction
                for child in stat:
                    child.text = d[child.tag]
                break
    mytree.write(dataFile, xml_declaration=True, encoding="UTF-8", method='xml')


def test():
    datFile = "D:\Workspace\python\myProjects\Bank\Bank\Data\instance\statementXML.xml"
    nameLine = "Volgnummer;Uitvoeringsdatum;Valutadatum;Bedrag;Valuta rekening;TEGENPARTIJ VAN DE VERRICHTING;Details;Rekeningnummer"
    dataLine = "2021-0074;09/10/2021;09/10/2021;-205.86;EUR;BETALING MET DEBETKAART         ;NUMMER 4871 04XX XXXX 5045 BRUSSELS AIRLINE  ZAVENTEM 09/10/2021 BANKREFERENTIE : 2110091631435778 VALUTADATUM : 09/10/2021;BE50001582721718"
    csvE = DataBank(nameLine, dataLine)
    # addStatement(datFile, csvE)
    a = getBankStatements(datFile)
    csvE.setAttr("Color", "blue")
    changeStatement(datFile, csvE)

