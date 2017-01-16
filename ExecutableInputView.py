import Tkinter

from EntryFactory import *
from LabelFactory import *

class ExecutableInputView(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)

        self.addHeaderRow()
        self.addEntriesRow()

    def addHeaderRow(self):
        fileRow = LabelFactory().createLabel(self, text="File")
        entries = [fileRow]

        for column, entry in enumerate(entries):
            entry.grid(row=0, column=column)

    def addEntriesRow(self):
        fileVar, fileEntry = EntryFactory().createFileEntry(self)
        entries = [fileEntry]

        for column, entry in enumerate(entries):
            entry.grid(row=1, column=column)

        self.fileVar = fileVar
