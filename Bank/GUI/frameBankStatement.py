from tkinter import *
from tkinter import ttk

from GUI.frameSuper import FrameSuper
from objects.dataBank import DataBank


class BankStatementFrame(FrameSuper):
    def __init__(self, parent, background, loc=None):
        super().__init__(parent, background, loc)

        self.styleCreate(parent)

        self.generateNew()
        # self.listbox = tk.Listbox(parent, selectmode="extended", width=120, height=25, exportselection=0)
        # self.listbox.pack(expand=1, fill="both")
        # self.listbox.grid(row=self.row, column=self.col, rowspan=3, columnspan=2)

        buttColor = ttk.Button(parent, text="Color", command=self.coloring)
        buttColor.grid(row=self.row+3, column=self.col+1, sticky=W)

        buttDecolor = ttk.Button(parent, text="Decolor", command=self.decoloring)
        buttDecolor.grid(row=self.row+3+1, column=self.col+1, sticky=W)

        self.varAutomate = IntVar()
        buttAutomate = ttk.Checkbutton(parent, text="Automate", variable=self.varAutomate, command=self.automate)
        buttAutomate.grid(row=self.row+3, column=self.col+0, sticky=E)


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
                self.bankTable.heading(col, text=col, anchor=CENTER)
            i = 0
            for tup in data:
                self.bankTable.insert(parent='', index='end', iid=str(i), text='', tags=[tup[0].getVolgNummer()],
                               values=tup[0].getGuiData())
                self.bankTable.tag_configure(tagname=tup[0].getVolgNummer(), background=tup[1])
                i += 1

    # generates new listbox
    def generateNew(self):
        # TODO: Find maybe a more efficienter method.
        """
        This are both bugged:
        ---
            for row in treeview.get_children():
                treeview.delete(row)
        ---
            treeview.delete(*treeview.get_children())
        ---
        """
        self.bankTable = ttk.Treeview(self.parent)
        self.bankTable.grid(row=self.row, column=self.col, rowspan=3, columnspan=2)
        self.generateTable()

    # event for generateNew
    def generateNewEvent(self, event):
        self.generateNew()

    """
    # adds a listbox, only do when data is already correct
    def addListbox(self, dat, index):
        if type(dat) is tuple and len(dat) == 2:
            self.listbox.insert(index, dat[0])
            self.listbox.itemconfig(index, bg=dat[1])

    # deletes listbox, only do when data is already removed
    def deleteListbox(self, index):
        self.listbox.delete(index, index)
    """

    # sort listbox on certain data element
    def sortStatements(self, event):
        self.background.sortBankStatements()
        self.generateNew()

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


