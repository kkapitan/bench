import subprocess32
import numpy as np

def prepParams(bin, perf, test):
    if perf == 0:
        return ["scripts/runTest", "run", "-bf", bin, "-pa", test[1], "-in", test[2], "-ou", test[3], "-t", test[4], "-m", test[5]]
    else:
        return ["scripts/runTest", "run", "-bf", bin, "-p", "aaa", "-pa", test[1], "-in", test[2], "-ou", test[3], "-t", test[4], "-m", test[5]]


def runTests(tests):
    res = []
    for test in tests[2:]:
        clkTick = []
        perfs = []
        times = []
        mems = []
        diffs = []
        exs = []
        for i in range(0, int(test[0])):
            subprocess32.call(prepParams(tests[0], tests[1], test))
            f=open("stat.stat")
            values=f.readline().split(";")
            f.close()
            clkTick += [values[0]]
            perfs += [values[1]]
            times += [values[2]]
            mems += [values[3]]
            diffs += [values[4]]
            exs += [values[5]]

        clkTicksAvg = np.average(np.array(clkTick).astype(np.float))
        perfsAvg = np.average(np.array(perfs).astype(np.float))
        timesAvg = np.average(np.array(times).astype(np.float))
        memsAvg = np.average(np.array(mems).astype(np.float))
        if "ERROR" in diffs:
            diffsRes = "ERROR"
        else :
            diffsRes = "OK"

        exsRes = 0
        for i in exs:
            if i != 0 and i != "0":
                exsRes = i
                break

        res += [[clkTicksAvg, perfsAvg, timesAvg, memsAvg, diffsRes, exsRes, test[3].split("/")[-1] ]]

    return res




