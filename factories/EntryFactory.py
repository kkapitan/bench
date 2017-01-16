import tkFileDialog
from Tkinter import *


class EntryFactory:

    def createArgumentsEntry(self, frame, initial="", width=None, readonly=False):
        var = StringVar()
        var.set(initial)

        entry = Entry(frame, textvariable=var)

        if readonly: entry.config(state="readonly")
        if width != None: entry.config(width=width)

        return var, entry

    def createFileEntry(self, frame, directory = '~'):
        var = StringVar(None)
        entry = Entry(frame, textvariable=var, state="readonly")
        entry.bind('<Button-1>', self.askFilename(frame, var, directory))

        return var, entry

    def askFilename(self, frame, var, directory):
        def callback(event):
            options = { 'initialdir' : directory, 'parent': frame, 'title' : 'This is a title'}
            var.set(tkFileDialog.askopenfilename(**options))
        return callback
