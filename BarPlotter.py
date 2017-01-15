import matplotlib
import numpy as np
matplotlib.use('TkAgg')

class BarPlotter():
  def __init__(self, times, mems, labels, timesStd, memsStd):
      self.times = times
      self.mems = mems
      self.labels = labels
      self.timesStd = timesStd
      self.memsStd = memsStd

  def plot(self, figure, clear=True):
    if clear:
        figure.clf()

    a = figure.add_subplot(111)

    t = np.arange(len(self.times))
    s = map(lambda x: float(x), self.times)
    m = map(lambda x: float(x), self.mems)
    ts = map(lambda x: float(x), self.timesStd)
    ms = map(lambda x: float(x), self.memsStd)
    width = 0.35

    a.bar(t, s, width, color='y', yerr=ts)
    a2 = a.twinx()
    a2.bar(t+width, m, width, color='r', yerr=ms)
    a2.set_ylabel('Memory')
    a.set_ylabel('Times')
    a.set_title('Bench results')
    a.set_xticks(map(lambda x: x + width, t))
    a.set_xticklabels(self.labels)
    a2.set_xticklabels(self.labels)