from MainView import *

if __name__=='__main__':
  root = Tkinter.Tk()

  MainView(root).pack()

  root.title("Bench by Krzysztof Kapitan & Jan Badura")
  root.resizable(0, 0)
  root.geometry("1200x900")

  root.mainloop()