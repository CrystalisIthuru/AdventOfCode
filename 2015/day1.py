import os

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "1.dat")

def parse_input(input_file):
    
    with open(input_file, "r") as f:
        return f.read().strip()
    
def run_elevator(source):
    
    floor = 0
    for char in source:
        if char == "(":
            floor += 1
        else:
            floor -= 1
    
    return floor

def first_basement(input):
    
    floor = 0
    for i, char in enumerate(input):
        if char == "(":
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            return i + 1

if __name__ == "__main__":
    
    input = parse_input(INPUT_FILE)
    print(run_elevator(input))
    print(first_basement(input))
