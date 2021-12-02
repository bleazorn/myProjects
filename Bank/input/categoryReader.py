import xml.etree.ElementTree as ET

from objects.dataCategory import DataCategory

categoryC = "Category"

# TODO: Generalize
# TODO: subcategory

# Get all categories.
# If parent exist, it will be all the subcategories
def getAllCategories(dataFile):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()

    return getCategory(myroot)

# Get all categories under parent. Either root or another category
def getCategory(parent):
    ret = []

    for cat in parent:
        if cat.tag == categoryC or cat.tag == DataCategory.subCategoryC:
            name = cat.find(DataCategory.nameC).text
            colo = cat.find(DataCategory.colorC).text

            subEle = cat.find(DataCategory.subCategoryC)
            sub = []
            if subEle:
                sub = getCategory(cat)

            catData = DataCategory(name, colo, sub)
            ret.append(catData)

    return ret


# Add a category to the given file. The category needs to have the DataCategory type.
# Can also be a subcategory, in this case parent is the name of the category.
# If layered it will be like this: sub1.sub2.sub3
def addCategory(dataFile, category, parent=None):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()

    splt = []
    if parent:
        splt = parent.split(".")

    newParent = myroot
    i = len(splt)
    for s in splt:
        for cat in newParent:
            if cat.tag == categoryC or cat.tag == DataCategory.subCategoryC:
                if s == cat.find(DataCategory.nameC).text:
                    newParent = cat
                    i -= 1
                    break

    isSubCat = parent is not None
    if isSubCat and i != 0:
        print("not found")
        return
    createCategoryElement(newParent, category, isSubCat)

    mytree.write(dataFile, xml_declaration=True, encoding="UTF-8", method='xml')


def createCategoryElement(parent, category, isSubCat=False):
    if not isinstance(category, DataCategory):
        return

    catN = categoryC
    if isSubCat:
        catN = DataCategory.subCategoryC

    ele = ET.SubElement(parent, catN)

    name = ET.SubElement(ele, DataCategory.nameC)
    name.text = category.getAttr(DataCategory.nameC)

    color = ET.SubElement(ele, DataCategory.colorC)
    color.text = category.getAttr(DataCategory.colorC)


# deletes a category in the given file with the given name
def deleteCategory(dataFile, categoryName):
    mytree = ET.parse(dataFile)
    myroot = mytree.getroot()

    cat, catRoot = getCategoryFromName(myroot, categoryName)
    if cat:
        catRoot.remove(cat)
        mytree.write(dataFile, xml_declaration=True, encoding="UTF-8", method='xml')


# get the category from the given name.
def getCategoryFromName(root, categoryName):
    for cat in root:
        if cat.tag == categoryC or cat.tag == DataCategory.subCategoryC:
            name = cat.find(DataCategory.nameC).text
            if name == categoryName:
                return cat, root
            subEle = cat.find(DataCategory.subCategoryC)
            if subEle:
                return getCategoryFromName(cat, categoryName)
    return None, None


def clearXMLText(text):
    pass


def test():
    test11 = "D:\Workspace\python\myProjects\Bank\\test\\testfiles\categoryXML.xml"
    print(getAllCategories(test11))
    deleteCategory(test11, "Health")
    print(getAllCategories(test11))
    # test1(test11)
    #test2(test11)


def test1(testN):
    addCategory(testN, DataCategory("Health", "red"), None)
    addCategory(testN, DataCategory("Food", "blue"), None)
    addCategory(testN, DataCategory("Entertainment", "green"), None)
    print(getAllCategories(testN))


def test2(testN):
    deleteCategory(testN, "Health")
    deleteCategory(testN, "Food")
    deleteCategory(testN, "Entertainment")
    print(getAllCategories(testN))

def test3():
    a = DataCategory("Health", "red")
    b = DataCategory("Food", "blue")
    c = DataCategory("Entertainment", "green")
    d = {}
    d[a] = [b, c]
    f = d.keys()
    for h in f:
        i = ""
    e = ""
