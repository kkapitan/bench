import subprocess32
import csv

from ArgumentsView import *
from DirectoryPickerView import *
from PlotView import *
from FilePickerView import *

class MainView(Tkinter.Frame):
  def __init__(self, root):
    Tkinter.Frame.__init__(self, root)

    self.executablePicker = FilePickerView(root, "Choose executable")
    self.executablePicker.pack()

    self.inputPicker = DirectoryPickerView(root, "Choose input directory", False)
    self.inputPicker.pack()

    self.argumentsView = ArgumentsView(root)
    self.argumentsView.pack()

    self.outputPicker = DirectoryPickerView(root, "Choose output directory")
    self.outputPicker.pack()

    self.executablePicker.fileName.set("ls")
    self.inputPicker.directory.set("/Users/kkapitan/bench/test")

    self.setupButton()

    self.plotCanvas = PlotView(root)
    self.plotCanvas.place()


  def setupButton(self):
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
    Tkinter.Button(self, text="Bench it!", command=self.main_action).pack(**button_opt)

  def main_action(self):

    inDir = self.inputPicker.directory.get()
    outDir = self.outputPicker.directory.get()
    args = self.argumentsView.arguments.get()
    cmd = self.executablePicker.fileName.get()

    pythonPath = "/usr/bin/python"
    benchPath = "./"
    benchCommand = 'bench.py --save res.csv --cases ' + inDir
    if outDir != None and len(outDir) > 0:
      benchCommand = benchCommand + ' --output ' + outDir
    benchCommand = benchCommand + ' ' + cmd
    if args != None and len(args) > 0:
      benchCommand = benchCommand + ' ' + args

    benchCommandArray = (pythonPath + ' ' + benchPath + benchCommand).split(" ")

    subprocess32.call(benchCommandArray)

    csvfile = open('res.csv', 'rb')
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')

    print benchCommandArray

    testNames = []
    testTimes = []
    for row in reader:
      testNames.append(row[0])
      testTimes.append(row[1])
    csvfile.close()

    self.plotCanvas.plot(testNames, testTimes)
