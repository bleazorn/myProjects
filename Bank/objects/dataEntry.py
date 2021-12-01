class DataEntry:
    def __init__(self, *att):
        self.diction = {}
        if len(att) == 1 and type(att[0]) is dict:
            self.diction = att[0]

    def getAttr(self, name):
        return self.diction[name]

    def setAttr(self, name, val):
        self.diction[name] = val