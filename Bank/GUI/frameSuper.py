class FrameSuper(object):
    def __init__(self, parent, loc):
        self.parent = parent
        self.row, self.col = self.getRowCol(loc)

    @staticmethod
    def getRowCol(loc):
        row = 0
        col = 0
        if loc and type(loc) is tuple and len(loc) == 2:
            row = loc[0]
            col = loc[1]
        return row, col
