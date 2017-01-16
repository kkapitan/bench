import Tkinter, Tkconstants
from BarPlotter import BarPlotter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class PlotView(Tkinter.Frame):
  def __init__(self, root):
    Tkinter.Frame.__init__(self, root)

    self.figure = f = Figure(figsize=(5, 4), dpi=100)

    self.canvas = canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tkconstants.TOP, fill=Tkconstants.BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tkconstants.TOP, fill=Tkconstants.BOTH, expand=1)

    def on_key_event(event):
      key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)

  def plot(self, labels, times, mems, timesStd, memsStd):
    BarPlotter(times, mems, labels, timesStd, memsStd).plot(self.figure)
    self.canvas.show()
