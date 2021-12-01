import xml.etree.ElementTree as ET

from objects.dataCategory import DataCategory

categoryC = "Category"
# TODO: Generalize
# TODO: subcategory

def getCategories(dataFile):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()

    ret = []

    for cat in myroot:
        d = {}
        d[DataCategory.nameC] = cat.find(DataCategory.nameC).text
        d[DataCategory.colorC] = cat.find(DataCategory.colorC).text
        ret.append(DataCategory(d))

    return ret


# Add a category to the given file. The category needs to have the DataCategory type.
# Can also be a subcategory, in this case parent is the name of the category.
def addCategory(dataFile, category, parent=None):
    if not isinstance(category, DataCategory):
        return
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()

    if not parent:
        parent = myroot
    ele = ET.SubElement(parent, categoryC)

    name = ET.SubElement(ele, DataCategory.nameC)
    name.text = category.getAttr(DataCategory.nameC)

    color = ET.SubElement(ele, DataCategory.colorC)
    color.text = category.getAttr(DataCategory.colorC)

    mytree.write(dataFile, xml_declaration=True, encoding="UTF-8", method='xml')


# deletes a category in the given file with the given name
def deleteCategory(dataFile, categoryName):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()
    for cat in myroot:
        name = cat.find(DataCategory.nameC).text
        if name == categoryName:
            myroot.remove(cat)
            break
    mytree.write(dataFile, xml_declaration=True, encoding="UTF-8", method='xml')


def clearXMLText(text):
    pass


def test():
    test11 = "D:\Workspace\python\myProjects\Bank\\test\\testfiles\categoryXML.xml"
    test21 = "D:\Workspace\python\myProjects\Bank\\test\\testfiles\\test.xml"
    test1(test11)
    # test2(test21)


def test1(testN):
    addCategory(testN, DataCategory("Health", "red"), None)
    addCategory(testN, DataCategory("Food", "blue"), None)
    addCategory(testN, DataCategory("Entertainment", "green"), None)
    print(getCategories(testN))


def test2(testN):
    deleteCategory(testN, "Health")
    deleteCategory(testN, "Food")
    deleteCategory(testN, "Entertainment")

test()
