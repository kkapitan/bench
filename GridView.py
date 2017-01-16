from EntryFactory import  *
from LabelFactory import *
from ButtonFactory import *

class GridView(Tkinter.Frame):
    def __init__(self, root, maxRows):
        Tkinter.Frame.__init__(self, root)
        self.userInputVars = []

        self.addHeaderRow()
        for i in range(1, maxRows + 1):
            self.addRow(i)

    def addHeaderRow(self):
        factory = LabelFactory()

        runsLabel = factory.createLabel(self, text="# of runs")
        argLabel = factory.createLabel(self, text="Shell args (optional)")

        inLabel = factory.createLabel(self, text="Input file")
        outLabel = factory.createLabel(self, text="Output file (optional)")

        timeLimitLabel = factory.createLabel(self, text="Timeout (s)")
        memLimitLabel = factory.createLabel(self, text="Memory limit (kB)")

        statusLabel = factory.createLabel(self, text="Status")

        entries = [runsLabel, argLabel, inLabel, outLabel, timeLimitLabel, memLimitLabel, statusLabel]

        for column, entry in enumerate(entries):
            entry.grid(row=0, column=column)

    def addRow(self, row):
        factory = EntryFactory()

        runsVar, runsEntry = factory.createArgumentsEntry(self, "1", 5)
        argVar, argEntry = factory.createArgumentsEntry(self)

        inVar, inEntry = factory.createFileEntry(self, './input')
        outVar, outEntry = factory.createFileEntry(self, './output')

        timeLimitVar, timeLimitEntry = factory.createArgumentsEntry(self, "1", 5)
        memLimitVar, memLimitEntry = factory.createArgumentsEntry(self, "1000000", 10)

        statusVar, statusEntry = factory.createArgumentsEntry(self, "Not Run", 10, True)

        entries = [runsEntry, argEntry, inEntry, outEntry, timeLimitEntry, memLimitEntry, statusEntry]

        for column, entry in enumerate(entries):
            entry.grid(row=row, column=column)

        vars = {"runs": runsVar, "args": argVar, "in": inVar, "out": outVar, "timelimit": timeLimitVar, "memlimit": memLimitVar, "status": statusVar}
        self.userInputVars.append(vars)

