from tkinter import *
from tkinter import ttk

from GUI.frameSuper import FrameSuper
from objects.dataBank import DataBank


class BankStatementFrame(FrameSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

        self.styleCreate(parent)

        self.bankTable = ttk.Treeview(self.parent)
        self.bankTable.grid(row=self.row, column=self.col, rowspan=3, columnspan=2)
        self.bankTable.bind('<Double-Button-1>', self.doubleClicked)

        self.doubleClick = False

        buttColor = ttk.Button(parent, text="Color", command=self.coloring)
        buttColor.grid(row=self.row+3, column=self.col+1, sticky=W)

        buttDecolor = ttk.Button(parent, text="Decolor", command=self.decoloring)
        buttDecolor.grid(row=self.row+3+1, column=self.col+1, sticky=W)

        self.varAutomate = IntVar()
        buttAutomate = ttk.Checkbutton(parent, text="Automate", variable=self.varAutomate, command=self.automate)
        buttAutomate.grid(row=self.row+3, column=self.col+0, sticky=E)

        self.generateTable()

    # don't delete this, this is for problems with python itself to be able to color things
    def styleCreate(self, parent):
        s = ttk.Style()

        # from os import name as OS_Name
        if parent.getvar('tk_patchLevel') == '8.6.9':  # and OS_Name=='nt':
            def fixed_map(option):
                # Fix for setting text colour for Tkinter 8.6.9
                # From: https://core.tcl.tk/tk/info/509cafafae
                #
                # Returns the style map for 'option' with any styles starting with
                # ('!disabled', '!selected', ...) filtered out.
                #
                # style.map() returns an empty list for missing options, so this
                # should be future-safe.
                return [elm for elm in s.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]

            s.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

    # creates the table from the data in the background
    def generateTable(self):
        data = self.background.getBankStatementsForGui()
        if len(data) > 0 and isinstance(data[0][0], DataBank):
            cols = data[0][0].getGuiCols()
            self.bankTable['columns'] = cols
            self.bankTable.column("#0", width=0, stretch=NO)
            self.bankTable.heading("#0", text="", anchor=CENTER)
            for col in cols:
                self.bankTable.column(col, anchor=CENTER, width=100)
                self.bankTable.heading(col, text=col, anchor=CENTER, command=lambda c=col: self.sortStatements(text=c))
                #
            self.generateRows(data)

    # generate rows for the bank table
    def generateRows(self, data):
        i = 0
        for tup in data:
            self.bankTable.insert(parent='', index='end', iid=str(i), text='', tags=[tup[0].getVolgNummer()],
                                  values=tup[0].getGuiData())
            self.bankTable.tag_configure(tagname=tup[0].getVolgNummer(), background=tup[1])
            i += 1

    # generates new listbox
    def generateNew(self):
        for row in self.bankTable.get_children():
            self.bankTable.delete(row)
        self.generateRows(self.background.getBankStatementsForGui())

    # event for generateNew
    def generateNewEvent(self, event):
        self.generateNew()

    def doubleClicked(self, event):
        self.doubleClick = True

    # sort listbox on certain data element
    def sortStatements(self, text):
        # self.background.sortBankStatements()
        if self.doubleClick:
            self.background.sortBankStatements(text)
            self.generateNew()
            self.doubleClick = False

    # returns the indexes of selected bankstatements
    def getSelecteds(self):
        # return self.listbox.curselection()
        return list(self.bankTable.selection())

    # Colors statement with index
    def colorStatement(self, name, coloring):
        self.bankTable.tag_configure(tagname=name, background=coloring)

    # Colors the selected bankstatemenst with the selected catogrie colors
    def coloring(self):
        self.getRoot().event_generate("<<Color>>")

    # makes the bankstatements colorless
    def decoloring(self):
        self.getRoot().event_generate("<<Decolor>>")

    def automate(self):
        if self.varAutomate.get():
            self.background.automate = True
        else:
            self.background.automate = False




def test():
    root = Tk()
    frm = ttk.Frame(root)
    frm.grid()
    banF = BankStatementFrame(frm, None)
    root.mainloop()


