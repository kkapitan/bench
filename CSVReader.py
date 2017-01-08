import csv

class CSVReader():

  def read(self, fileName):
    csvfile = open(fileName, 'rb')
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')

    contents = zip(*reader)
    csvfile.close()
    return contents
