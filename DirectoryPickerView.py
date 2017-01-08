import Tkinter, Tkconstants, tkFileDialog
from Tkinter import *

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

    Checkbutton(self, text="Add expected output", variable=stateVar, onvalue=1, offvalue=0, command=cb).pack()
    cb()

  def setupEntry(self):
    entry_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    entry = Entry(self, textvariable=self.directory)
    entry.pack(**entry_opt)
    entry.configure(state="disabled")

  def setupButton(self, text, command):
    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    button = Tkinter.Button(self, text=text, command=command)
    button.pack(**button_opt)
    return button

  def askDirectory(self):
    options = {'initialdir': '~', 'mustexist': False,'parent':self,'title':'This is a title'}

    self.directory.set(tkFileDialog.askdirectory(**options))
