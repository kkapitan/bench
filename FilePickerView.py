import Tkinter, Tkconstants, tkFileDialog
from Tkinter import *

class FilePickerView(Tkinter.Frame):

  def __init__(self, root, name):
    Tkinter.Frame.__init__(self, root)
    self.fileName = StringVar(0)

    self.setupEntry()

  def setupEntry(self):
      entry_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

      entry = Entry(self, textvariable=self.fileName, state="readonly")
      entry.pack(**entry_opt)
      entry.bind('<Button-1>', self.askFilename)

      return entry

  def askFilename(self, event):
    options = { 'initialdir' : '~', 'parent': self, 'title' : 'This is a title'}
    self.fileName.set(tkFileDialog.askopenfilename(**options))
