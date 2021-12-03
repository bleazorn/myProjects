from objects.dataEntry import DataEntry


class DataCategory(DataEntry):
    nameC = "Name"
    colorC = "Color"
    subCategoryC = "SubCategory"
    parentC = "parent"

    def __init__(self, *args):
        super().__init__(*args)
        if len(args) == 2:
            self.setAttr(DataCategory.nameC, args[0])
            self.setAttr(DataCategory.colorC, args[1])
            self.setAttr(DataCategory.subCategoryC, [])
            self.setAttr(DataCategory.parentC, "")

        elif len(args) == 3 and type(args[2]) == list:
            self.setAttr(DataCategory.nameC, args[0])
            self.setAttr(DataCategory.colorC, args[1])
            self.setAttr(DataCategory.subCategoryC, args[2])
            self.setAttr(DataCategory.parentC, "")

        elif len(args) == 4 and type(args[2]) == list:
            self.setAttr(DataCategory.nameC, args[0])
            self.setAttr(DataCategory.colorC, args[1])
            self.setAttr(DataCategory.subCategoryC, args[2])
            self.setAttr(DataCategory.parentC, args[3])

    def getName(self):
        return self.getAttr(DataCategory.nameC)

    def getColor(self):
        return self.getAttr(DataCategory.colorC)

    def getSubCategory(self):
        return self.getAttr(DataCategory.subCategoryC)

    def getParent(self):
        return self.getAttr(DataCategory.parentC)

    def getFullName(self):
        fullName = self.getName()
        if self.getParent():
            fullName = self.getParent() + "." + fullName
        return fullName

    def __repr__(self):
        return self.getAttr(DataCategory.nameC)

    def __str__(self):
        return self.getAttr(DataCategory.nameC)
