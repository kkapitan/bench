import Tkinter, Tkconstants
from Tkinter import *

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

    Checkbutton(self, text="Add command line arguments", variable=stateVar, onvalue=1, offvalue=0, command=cb).pack()
    cb()

  def setupEntry(self):
    entry_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

    entry = Entry(self, textvariable=self.arguments)
    entry.pack(**entry_opt)
    entry.configure(state="disabled")

    return entry