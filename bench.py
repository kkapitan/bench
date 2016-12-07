import argparse
import subprocess32

__author__ = "Krzysztof Kapitan & Jan Badura"


def main():
    parser = argparse.ArgumentParser(description='Run tests and measure the time')
    parser.add_argument('--path', dest='path_to_executable', required=True, nargs="?",
                        type=str, help='path to executable')
    parser.add_argument('--cases', dest='path_to_test_cases', required=True, nargs="?",
                        type=str, help='path to test cases')
    parser.add_argument('--output', dest="path_to_test_output", required=False, nargs="?",
                        type=str, help='path to test output')

    args = parser.parse_args()

    file_output = open("test.txt", "w")

    executable = args.path_to_executable
    print(subprocess32.call(["ls"], timeout=1, stdout=file_output))

if __name__ == '__main__':
    main()