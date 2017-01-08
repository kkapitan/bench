class BenchCommandBuilder():

  def buildCommandString(self, inDir, outDir, cmd, args):
    pythonPath = "/usr/bin/python"
    benchPath = "./"

    benchCommand = 'bench.py --save res.csv --cases ' + inDir

    if outDir != None and len(outDir) > 0:
      benchCommand = benchCommand + ' --output ' + outDir

    benchCommand = benchCommand + ' ' + cmd

    if args != None and len(args) > 0:
      benchCommand = benchCommand + ' ' + args

    return pythonPath + ' ' + benchPath + benchCommand

  def buildCommand(self, inDir, outDir, cmd, args):
      return self.buildCommandString(inDir, outDir, cmd, args).split(" ")

