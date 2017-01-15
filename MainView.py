import subprocess32

from Runner import *
import Tkinter, Tkconstants, tkFileDialog
from Tkinter import *

from PlotView import *
from BenchCommandBuilder import *
from CSVReader import *

class BinaryInputView(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)

        self.addHeaderRow()
        self.addRow(1)

    def addHeaderRow(self):

        fileRow = Label(self, text="File")

        entries = [fileRow]

        for column, entry in enumerate(entries):
            entry.grid(row=0, column=column)

    def addRow(self, row):

        fileVar, fileEntry = self.setupFileEntry()
        entries = [fileEntry]

        for column, entry in enumerate(entries):
            entry.grid(row=row, column=column)

        self.fileVar = fileVar

    def setupFileEntry(self):
        var = StringVar(None)
        entry = Entry(self, textvariable=var, state="readonly")
        entry.bind('<Button-1>', self.askFilename(var))

        return var, entry

    def askFilename(self, var):
        def callback(event):
            options = {'initialdir': '~', 'parent': self, 'title': 'This is a title'}
            var.set(tkFileDialog.askopenfilename(**options))

        return callback


class GridView(Tkinter.Frame):
    def __init__(self, root, maxRows):
        Tkinter.Frame.__init__(self, root)
        self.userInputVars = []

        self.addHeaderRow()
        for i in range(1, maxRows + 1):
            self.addRow(i)

        self.number_of_rows = maxRows

    def addHeaderRow(self):

        runsLabel = Label(self, text="# of runs")
        argLabel = Label(self, text="Shell args (optional)")
        inLabel = Label(self, text="Input file")
        outLabel = Label(self, text="Output file (optional)")
        timeLimitLabel = Label(self, text="Timeout (s)")
        memLimitLabel = Label(self, text="Memory limit (kB)")
        statusLabel = Label(self, text="Status")

        entries = [runsLabel, argLabel, inLabel, outLabel, timeLimitLabel, memLimitLabel, statusLabel]

        for column, entry in enumerate(entries):
            entry.grid(row=0, column=column)

    def addRow(self, row):

        runsVar, runsEntry = self.argumentsEntry("1", 5)
        argVar, argEntry = self.argumentsEntry()
        inVar, inEntry = self.setupFileEntry()
        outVar, outEntry = self.setupFileEntry()
        timeLimitVar, timeLimitEntry = self.argumentsEntry("1", 5)
        memLimitVar, memLimitEntry = self.argumentsEntry("1000000", 10)
        statusVar, statusEntry = self.argumentsEntry("Not Run", 10, True)

        entries = [runsEntry, argEntry, inEntry, outEntry, timeLimitEntry, memLimitEntry, statusEntry]

        for column, entry in enumerate(entries):
            entry.grid(row=row, column=column)

        vars = {"runs": runsVar, "args": argVar, "in": inVar, "out": outVar, "timelimit": timeLimitVar, "memlimit": memLimitVar, "status": statusVar}
        self.userInputVars.append(vars)


    def argumentsEntry(self, initial="", width=None, readonly=False):
        var = StringVar()
        var.set(initial)

        entry = Entry(self, textvariable=var)
        if readonly: entry.config(state="readonly")
        if width != None: entry.config(width=width)
        return var, entry

    def setupFileEntry(self):
        var = StringVar(None)
        entry = Entry(self, textvariable=var, state="readonly")
        entry.bind('<Button-1>', self.askFilename(var))

        return var, entry

    def askFilename(self, var):
        def callback(event):
            options = { 'initialdir' : '~', 'parent': self, 'title' : 'This is a title'}
            var.set(tkFileDialog.askopenfilename(**options))
        return callback

class MainView(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)

        self.fileInputView = fi = BinaryInputView(self)
        fi.pack()

        self.gridView = gv = GridView(self, 5)
        gv.pack()

        self.plotView = pv = PlotView(self)
        pv.pack()

        button = self.setupButton("Bench it!", self.main_action)
        button.pack()

    def main_action(self):
        params = self.prepare_input()

        res = runTests(params)
        resT = zip(*res)
        print resT
        self.plotView.plot(resT[6], resT[1], resT[3], resT[7], resT[9])
        self.prepare_output(resT[4])

    def prepare_input(self):

        file = self.fileInputView.fileVar.get()
        result = [file, '1']

        for inputDictionary in self.gridView.userInputVars:
            resultEntry = map(lambda x: inputDictionary[x].get(), ["runs", "args", "in", "out", "timelimit", "memlimit"])
            result.append(resultEntry)

        return result

    def prepare_output(self, result):
        self.plotView.plot(result[-1], result[0], result[3])
        self.output_statuses(["OK", "ERROR"])

    def output_statuses(self, statuses):
        for index, status in enumerate(statuses):
            self.gridView.userInputVars[index]["status"].set(status)

    def setupButton(self, text, command):
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

        button = Tkinter.Button(self, text=text, command=command)
        button.pack(**button_opt)
        return button