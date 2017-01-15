import subprocess32

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

        entries = [runsLabel, argLabel, inLabel, outLabel, timeLimitLabel, memLimitLabel]

        for column, entry in enumerate(entries):
            entry.grid(row=0, column=column)

    def addRow(self, row):

        runsVar, runsEntry = self.argumentsEntry("10", 5)
        argVar, argEntry = self.argumentsEntry()
        inVar, inEntry = self.setupFileEntry()
        outVar, outEntry = self.setupFileEntry()
        timeLimitVar, timeLimitEntry = self.argumentsEntry("5", 5)
        memLimitVar, memLimitEntry = self.argumentsEntry("1000000", 10)

        entries = [runsEntry, argEntry, inEntry, outEntry, timeLimitEntry, memLimitEntry]

        for column, entry in enumerate(entries):
            entry.grid(row=row, column=column)

        vars = {"runs": runsVar, "args": argVar, "in": inVar, "out": outVar, "timelimit": timeLimitVar, "memlimit": memLimitVar}
        self.userInputVars.append(vars)


    def argumentsEntry(self, initial="", width=None):
        var = StringVar()
        var.set(initial)

        entry = Entry(self, textvariable=var)
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

        self.gridView = gv = GridView(self, 10)
        gv.pack()

        self.plotView = pv = PlotView(self)
        pv.pack()

        button = self.setupButton("Bench it!", self.main_action)
        button.pack()

    def main_action(self):
        print(self.prepare_input())

        #subprocess32.call(BenchCommandBuilder().buildCommand(inDir, outDir, cmd, args))

        array = CSVReader().read("res.csv")
        self.plotView.plot(array[0], array[1])

    def prepare_input(self):

        file = self.fileInputView.fileVar.get()
        result = [file, '1']

        for inputDictionary in self.gridView.userInputVars:
            resultEntry = map(lambda x: inputDictionary[x].get(), ["runs", "args", "in", "out", "timelimit", "memlimit"])
            result.append(resultEntry)

        return result

    def setupButton(self, text, command):
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

        button = Tkinter.Button(self, text=text, command=command)
        button.pack(**button_opt)
        return button