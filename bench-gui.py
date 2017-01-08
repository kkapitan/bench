import Tkinter, Tkconstants, tkFileDialog
from Tkinter import *

import os, csv, matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import subprocess32

class DirectoryPickerView(Tkinter.Frame):

  def __init__(self, root, name, show_checkbox=True):
    Tkinter.Frame.__init__(self, root)
    self.directory = StringVar(None)

    self.setupEntry()
    button = self.setupButton(name, self.askDirectory)

    if show_checkbox:
      self.checkState = IntVar(None)
      self.setupCheckbox(self.checkState, button)

  def setupCheckbox(self, stateVar, widget):
    def cb():
      if self.checkState.get() == 0:
        widget.config(state="disabled")
        self.directory.set("")
      else:
        widget.config(state="normal")

    Checkbutton(root, text="Add expected output", variable=stateVar, onvalue=1, offvalue=0, command=cb).pack()
    cb()

  def setupEntry(self):
    entry_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    entry = Entry(root, textvariable=self.directory)
    entry.pack(**entry_opt)
    entry.configure(state="disabled")

  def setupButton(self, text, command):
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    button = Tkinter.Button(self, text=text, command=command)
    button.pack(**button_opt)
    return button

  def askDirectory(self):
    options = {'initialdir': '~', 'mustexist': False,'parent':root,'title':'This is a title'}

    self.directory.set(tkFileDialog.askdirectory(**options))

class FilePickerView(Tkinter.Frame):

  def __init__(self, root, name):
    Tkinter.Frame.__init__(self, root)
    self.fileName = StringVar(0)

    self.setupEntry()
    self.setupButton(name, self.askFilename)

  def setupEntry(self):
    entry_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    entry = Entry(root, textvariable=self.fileName)
    entry.pack(**entry_opt)
    entry.configure(state="disabled")

  def setupButton(self, text, command):
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    Tkinter.Button(self, text=text, command=command).pack(**button_opt)

  def askFilename(self):
    options = {'filetypes' : [('all files', '.*'), ('text files', '.txt')], 'initialdir' : '~', 'parent': root, 'title' : 'This is a title'}
    self.fileName.set(tkFileDialog.askopenfilename(**options))



class ArgumentsView(Tkinter.Frame):

  def __init__(self, root):
    Tkinter.Frame.__init__(self, root)
    self.arguments = StringVar(None)

    entry = self.setupEntry()

    self.checkState = IntVar(None)
    self.setupCheckbox(self.checkState, entry)

  def setupCheckbox(self, stateVar, widget):
    def cb():
      if self.checkState.get() == 0:
        widget.config(state="disabled")
        self.arguments.set("")
      else:
        widget.config(state="normal")

    Checkbutton(root, text="Add command line arguments", variable=stateVar, onvalue=1, offvalue=0, command=cb).pack()
    cb()

  def setupEntry(self):
    entry_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    entry = Entry(root, textvariable=self.arguments)
    entry.pack(**entry_opt)
    entry.configure(state="disabled")

    return entry

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
    s = map(lambda x: float(x), yvals)

    width = 0.35

    a.bar(t, s, width)
    a.set_ylabel('Times')
    a.set_title('Bench results')
    a.set_xticks(map(lambda x: x + width,t))
    a.set_xticklabels(xvals)

    self.canvas.show()


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

    self.plotCanvas = TkPlotCanvas(root)
    self.plotCanvas.place()


  def setupButton(self):
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
    Tkinter.Button(root, text="Bench it!", command=self.main_action).pack(**button_opt)

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

def is_exe(fpath):
  return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

if __name__=='__main__':
  root = Tkinter.Tk()
  MainView(root).place()
  root.title("Bench by Krzysztof Kapitan & Jan Badura")
  root.resizable(0, 0)
  root.geometry("500x900")

  root.mainloop()