import numpy as np

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

    rects1 = a.bar(t, s, width, color='y', yerr=ts)
    a2 = a.twinx()
    rects2 = a2.bar(t+width, m, width, color='r', yerr=ms)

    a2.set_ylabel('Memory[kB]')
    a.set_ylabel('Times[s]')

    a.set_title('Bench results')
    a.set_xticks(map(lambda x: x + width, t))

    a.set_xticklabels(self.labels)
    a2.set_xticklabels(self.labels)

    a.set_ylim(bottom=0)
    a2.set_ylim(bottom=0)

    def autolabel(rects, ax):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%.2f' % float(height),
                    ha='center', va='bottom')

    autolabel(rects1, a)
    autolabel(rects2, a2)
