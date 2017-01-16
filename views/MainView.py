from ExecutableInputView import *
from GridView import *
from PlotView import *

from factories.ButtonFactory import *

from tools.Runner import *


class MainView(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)

        self.fileInputView = fi = ExecutableInputView(self)
        fi.pack()

        self.gridView = gv = GridView(self, 5)
        gv.pack()

        self.plotView = pv = PlotView(self)
        pv.pack()

        button = ButtonFactory().createButton(self, "Bench it!", self.main_action)
        button.pack({'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5})

    def main_action(self):
        params = self.prepare_input()

        print params
        res = runTests(params)
        #res = self.mock_data(5)
        resT = zip(*res)

        self.prepare_output(resT)

    def prepare_input(self):

        file = self.fileInputView.fileVar.get()
        result = [file, '0']

        for inputDictionary in self.gridView.userInputVars:
            resultEntry = map(lambda x: inputDictionary[x].get(), ["runs", "args", "in", "out", "timelimit", "memlimit"])
            if resultEntry[2] != '':
                result.append(resultEntry)

        return result

    def prepare_output(self, result):
        print result
        self.plotView.plot(result[6], result[2], result[3], result[8], result[9])
        self.output_statuses(result[-1])

    def output_statuses(self, statuses):
        for index, status in enumerate(statuses):
            self.gridView.userInputVars[index]["status"].set(status)

    # Data only for mocking
    def mock_data(self, number_of_entries):
        def mock_entry(x):
            return [0.0, x * 5.0, 0.0, x * 256.0, 'OK', '127', 'case ' + str(x), 10.0, 0.0, 5.0,'OK']
        return map(mock_entry, range(1, number_of_entries + 1))
