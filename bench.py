import argparse
import subprocess32
import time
import os
import csv

__author__ = "Krzysztof Kapitan & Jan Badura"

def main():
    parser = argparse.ArgumentParser(description='Run tests and measure the time')
    parser.add_argument('--cases', dest='path_to_test_cases', required=True, nargs="?",
                        type=str, help='path to test cases')
    parser.add_argument('--output', dest="path_to_test_output", required=False, nargs="?",
                        type=str, help='path to test output')
    parser.add_argument('--save', dest="results_destination", required=False, default="results.csv", nargs="?",
                        type=str, help='save results destination')

    args, executable = parser.parse_known_args()
    file_output = open("test.txt", "w")

    times = []
    resultsFilename = args.results_destination
    for file in os.listdir(args.path_to_test_cases):
        if file.endswith(".txt"):
            start = time.time()
            subprocess32.call(executable, stdout=file_output)
            end = time.time()

            times.append((file, end - start))

    csvfile = open(resultsFilename, 'wb')
    timeswriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for entry in times:
        timeswriter.writerow(entry)

    csvfile.close()

if __name__ == '__main__':
    main()