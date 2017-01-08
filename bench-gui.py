import Tkinter, Tkconstants, tkFileDialog
from Tkinter import *

import os, csv

import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import subprocess32

class DirectoryPickerView(Tkinter.Frame):

  def __init__(self, root, name):
    Tkinter.Frame.__init__(self, root)
    self.directory = StringVar(None)

    self.setupEntry()
    self.setupButton(name, self.askDirectory)

  def setupEntry(self):
    entry_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    Entry(root, textvariable=self.directory).pack(**entry_opt)

  def setupButton(self, text, command):
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    Tkinter.Button(self, text=text, command=command).pack(**button_opt)

  def askDirectory(self):
    options = {'initialdir': '~', 'mustexist': False,'parent':root,'title':'This is a title'}

    self.directory.set(tkFileDialog.askdirectory(**options))

class FilePickerView(Tkinter.Frame):

  def __init__(self, root, name):
    Tkinter.Frame.__init__(self, root)
    self.fileName = StringVar(None)

    self.setupEntry()
    self.setupButton(name, self.askFilename)

  def setupEntry(self):
    entry_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    Entry(root, textvariable=self.fileName).pack(**entry_opt)

  def setupButton(self, text, command):
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    Tkinter.Button(self, text=text, command=command).pack(**button_opt)

  def askFilename(self):
    options = {'filetypes' : [('all files', '.*'), ('text files', '.txt')], 'initialdir' : '~', 'parent': root, 'title' : 'This is a title'}
    self.fileName.set(tkFileDialog.askopenfilename(**options))

class TkPlotCanvas(Tkinter.Frame):
  def __init__(self, root):
    Tkinter.Frame.__init__(self, root)

    self.f = f = Figure(figsize=(5, 4), dpi=100)

    self.canvas = canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tkconstants.TOP, fill=Tkconstants.BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tkconstants.TOP, fill=Tkconstants.BOTH, expand=1)

    def on_key_event(event):
      print('you pressed %s' % event.key)
      key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)

  def plot(self, xvals, yvals):
    f = self.f
    f.clf()

    a = f.add_subplot(111)
    t = range(0, len(yvals), 1)
    s = yvals

    a.plot(t, s)

    self.canvas.show()


class MainView(Tkinter.Frame):
  def __init__(self, root):
    Tkinter.Frame.__init__(self, root)

    self.executablePicker = FilePickerView(root, "Choose executable")
    self.executablePicker.pack()

    self.inputPicker = DirectoryPickerView(root, "Choose input directory")
    self.inputPicker.pack()

    self.outputPicker = DirectoryPickerView(root, "Choose output directory")
    self.outputPicker.pack()

    self.executablePicker.fileName.set("ls")
    self.inputPicker.directory.set("/Users/kkapitan/bench/test")

    self.plotCanvas = TkPlotCanvas(root)
    self.plotCanvas.place()

    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
    Tkinter.Button(root, text="Bench it!", command=self.main_action).pack(**button_opt)

  def main_action(self):

    inDir = self.inputPicker.directory.get()
    outDir = self.outputPicker.directory.get()
    cmd = self.executablePicker.fileName.get()

    pythonPath = "/usr/bin/python"
    benchPath = "./"
    benchCommand = 'bench.py --save res.csv --cases ' + inDir
    if outDir != None and len(outDir) > 0:
      benchCommand = benchCommand + ' --output ' + outDir
    benchCommand = benchCommand + ' ' + cmd

    benchCommandArray = (pythonPath + ' ' + benchPath + benchCommand).split(" ")

    subprocess32.call(benchCommandArray)

    csvfile = open('res.csv', 'rb')
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')

    testNames = []
    testTimes = []
    for row in reader:
      testNames.append(row[0])
      testTimes.append(row[1])
    csvfile.close()

    self.plotCanvas.plot(testNames, testTimes)

def is_exe(fpath):
  return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

if __name__=='__main__':
  root = Tkinter.Tk()
  MainView(root).place()
  root.mainloop()