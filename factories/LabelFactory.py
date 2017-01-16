from Tkinter import *


class LabelFactory:

    def createLabel(self, frame, text):
        return Label(frame, text=text)
