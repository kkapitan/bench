import subprocess32
import numpy as np

def prepParams(bin, perf, test):
    command = []
    command += ["scripts/runTest"]
    command += ["run"]
    command += ["-bf"]
    command += [bin]
    if perf == "1":
        command += ["-p"]
        command += ["true"]
    if test[1] != "":
        command += ["-pa"]
        command += [test[1]]
    if test[1] == "":
        command += ["-pa"]
        command += ["null"]
    if test[2] != "":
        command += ["-in"]
        command += [test[2]]
    if test[3] != "":
        command += ["-ou"]
        command += [test[3]]
    if test[4] != "":
        command += ["-t"]
        command += [test[4]]
    if test[5] != "":
        command += ["-m"]
        command += [test[5]]

    return command

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
        perfstdDev = np.std(np.array(perfs).astype(np.float))
        timesAvg = np.average(np.array(times).astype(np.float))
        timesStdDev = np.std(np.array(times).astype(np.float))
        memsAvg = np.average(np.array(mems).astype(np.float))
        memStdDev = np.std(np.array(mems).astype(np.float))
        if "ERROR" in diffs:
            diffsRes = "ERROR"
        else :
            diffsRes = "OK"

        exsRes = 0
        for i in exs:
            if i != 0 and i != "0":
                exsRes = i
                break
        name = test[3].split("/")[-1]
        if name == "":
            name = "case"
        res += [[clkTicksAvg, perfsAvg, timesAvg, memsAvg, diffsRes, exsRes, name, perfstdDev, timesStdDev, memStdDev ]]

    return res




