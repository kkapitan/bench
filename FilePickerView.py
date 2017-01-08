import Tkinter, Tkconstants, tkFileDialog
from Tkinter import *

class FilePickerView(Tkinter.Frame):

  def __init__(self, root, name):
    Tkinter.Frame.__init__(self, root)
    self.fileName = StringVar(0)

    self.setupEntry()
    self.setupButton(name, self.askFilename)

  def setupEntry(self):
    entry_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    entry = Entry(self, textvariable=self.fileName)
    entry.pack(**entry_opt)
    entry.configure(state="disabled")

  def setupButton(self, text, command):
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    Tkinter.Button(self, text=text, command=command).pack(**button_opt)

  def askFilename(self):
    options = {'filetypes' : [('all files', '.*'), ('text files', '.txt')], 'initialdir' : '~', 'parent': root, 'title' : 'This is a title'}
    self.fileName.set(tkFileDialog.askopenfilename(**options))
