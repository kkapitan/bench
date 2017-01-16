import Tkinter

class ButtonFactory:

    def createButton(self, frame, text, command):
        return Tkinter.Button(frame, text=text, command=command)

