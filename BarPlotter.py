import matplotlib
import numpy as np
matplotlib.use('TkAgg')

class BarPlotter():
  def __init__(self, times, mems, labels):
      self.times = times
      self.mems = mems
      self.labels = labels

  def plot(self, figure, clear=True):
    if clear:
        figure.clf()

    a = figure.add_subplot(111)

    t = np.arange(len(self.times))
    s = map(lambda x: float(x), self.times)
    m = map(lambda x: float(x), self.mems)

    width = 0.35

    a.bar(t, s, width)
    a.bar(t+width, m, width, color='r')
    a.set_ylabel('Times')
    a.set_title('Bench results')
    a.set_xticks(map(lambda x: x + width, t))
    a.set_xticklabels(self.labels)