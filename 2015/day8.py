import os

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "8.dat")

def parse_input(input_file):

    strings = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            strings += [(line, eval(line))]
    
    return strings

def encoded_length(string):

    return len(string) + string.count("\\") + string.count("\"") + 2

if __name__ == "__main__":

    strings = parse_input(INPUT_FILE)
    print(sum(map(lambda string: len(string[0]) - len(string[1]), strings)))
    print(sum(map(lambda string: encoded_length(string[0]) - len(string[0]), strings)))