import xml.etree.ElementTree as ET


def getCategories(dataFile):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()
    ret = []

    for cat in myroot:
        name = cat.find("Name").text
        color = cat.find("Color").text
        ret.append((name, color))

    return ret


def addCategory(dataFile, category, parent=None):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()

    if not parent:
        parent = myroot

    ele = ET.SubElement(parent, "Category")

    name = ET.SubElement(ele, "Name")
    name.text = category[0]

    color = ET.SubElement(ele, "Color")
    color.text = category[1]

    mytree.write(dataFile, xml_declaration=True, encoding="UTF-8", method='xml')


def deleteCategory(dataFile, category):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()
    for cat in myroot:
        name = cat.find("Name").text
        if name == category:
            myroot.remove(cat)
            break
    mytree.write(dataFile, xml_declaration=True, encoding="UTF-8", method='xml')


def clearXMLText(text):
    pass


def test1(test):
    addCategory(test, ("Health", "red"), None)
    addCategory(test, ("Food", "blue"), None)
    addCategory(test, ("Entertainment", "green"), None)
    print(getCategories(test))


def test2(test):
    deleteCategory(test, "Health")
    deleteCategory(test, "Food")
    deleteCategory(test, "Entertainment")


test11 = "D:\Workspace\python\myProjects\Bank\\test\\testfiles\categoryXML.xml"
test21 = "D:\Workspace\python\myProjects\Bank\\test\\testfiles\\test.xml"
#test1(test21)
#test2(test21)
