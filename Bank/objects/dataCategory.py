from objects.dataEntry import DataEntry


class DataCategory(DataEntry):
    nameC = "Name"
    colorC = "Color"

    def __init__(self, *args):
        super().__init__(*args)
        b = len(args)
        d = type(args)
        if len(args) == 2:
            self.setAttr(DataCategory.nameC, args[0])
            self.setAttr(DataCategory.colorC, args[1])

    def __repr__(self):
        return self.getAttr(DataCategory.nameC)

    def __str__(self):
        return self.getAttr(DataCategory.nameC)
