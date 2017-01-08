import Tkinter, Tkconstants

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class PlotView(Tkinter.Frame):
  def __init__(self, root):
    Tkinter.Frame.__init__(self, root)

    self.f = f = Figure(figsize=(5, 4), dpi=100)

    self.canvas = canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tkconstants.TOP, fill=Tkconstants.BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tkconstants.TOP, fill=Tkconstants.BOTH, expand=1)

    def on_key_event(event):
      print('you pressed %s' % event.key)
      key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)

  def plot(self, xvals, yvals):
    f = self.f
    f.clf()

    a = f.add_subplot(111)

    t = range(0, len(yvals), 1)
    s = map(lambda x: float(x), yvals)

    width = 0.35

    a.bar(t, s, width)
    a.set_ylabel('Times')
    a.set_title('Bench results')
    a.set_xticks(map(lambda x: x + width,t))
    a.set_xticklabels(xvals)

    self.canvas.show()
