import argparse
import subprocess32
import time
import os
import csv

__author__ = "Krzysztof Kapitan & Jan Badura"

def process_directory(path, expected_format):
    print(path, expected_format)
    return map(lambda x: x.split(".")[0], filter(lambda x: x.endswith(expected_format), os.listdir(path)))

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

    resultsFilename = args.results_destination
    has_outputs = args.path_to_test_output != None

    times = []
    output_files = []
    if has_outputs:
        output_files = process_directory(args.path_to_test_output, ".out")

    input_files = process_directory(args.path_to_test_cases, ".in")

    for file in input_files:
        has_expected_output = output_files.__contains__(file)
        print(file, has_expected_output)

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