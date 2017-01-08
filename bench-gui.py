from MainView import *

if __name__=='__main__':
  root = Tkinter.Tk()
  MainView(root).place()
  root.title("Bench by Krzysztof Kapitan & Jan Badura")
  root.resizable(0, 0)
  root.geometry("500x900")

  root.mainloop()