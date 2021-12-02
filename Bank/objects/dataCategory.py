from objects.dataEntry import DataEntry


class DataCategory(DataEntry):
    nameC = "Name"
    colorC = "Color"
    subCategoryC = "SubCategory"

    def __init__(self, *args):
        super().__init__(*args)
        if len(args) == 2:
            self.setAttr(DataCategory.nameC, args[0])
            self.setAttr(DataCategory.colorC, args[1])
            self.setAttr(DataCategory.subCategoryC, [])

        if len(args) == 3 and type(args[2]) == list:
            self.setAttr(DataCategory.nameC, args[0])
            self.setAttr(DataCategory.colorC, args[1])
            self.setAttr(DataCategory.subCategoryC, args[2])

    def getName(self):
        return self.getAttr(DataCategory.nameC)

    def getColor(self):
        return self.getAttr(DataCategory.colorC)

    def getSubCategory(self):
        return self.getAttr(DataCategory.subCategoryC)

    def __repr__(self):
        return self.getAttr(DataCategory.nameC)

    def __str__(self):
        return self.getAttr(DataCategory.nameC)
