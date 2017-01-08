import matplotlib
matplotlib.use('TkAgg')

class BarPlotter():
  def __init__(self, vals, labels):
      self.vals = vals
      self.labels = labels

  def plot(self, figure, clear=True):
    if clear:
        figure.clf()

    a = figure.add_subplot(111)

    t = range(0, len(self.vals), 1)
    s = map(lambda x: float(x), self.vals)

    width = 0.35

    a.bar(t, s, width)
    a.set_ylabel('Times')
    a.set_title('Bench results')
    a.set_xticks(map(lambda x: x + width, t))
    a.set_xticklabels(self.labels)