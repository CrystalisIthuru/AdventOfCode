import numpy as np
import os
import re

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "9.dat")

def parse_input(input_file):

    sequences = []
    with open(input_file, "r") as f:
        for line in f:
            if line.strip() == "": continue
            sequences += [np.array([int(n) for n in re.findall(r"-?\d+", line)])]

    return sequences

def find_next_element(sequence):

    derivatives = [sequence]
    current_derivative = sequence
    while np.any(current_derivative != 0):
        
        current_derivative = np.diff(current_derivative)
        derivatives += [current_derivative]

    next_element = 0
    for derivative in derivatives:
        next_element += derivative[-1]

    return next_element

def find_previous_element(sequence):
 
    derivatives = [sequence]
    current_derivative = sequence
    while np.any(current_derivative != 0):
        
        current_derivative = np.diff(current_derivative)
        derivatives += [current_derivative]

    next_element = 0
    for derivative in reversed(derivatives):
        next_element = derivative[0] - next_element

    return next_element

if __name__ == "__main__":

    sequences = parse_input(INPUT_FILE)

    print(sum([find_next_element(S) for S in sequences]))
    print(sum([find_previous_element(S) for S in sequences]))
