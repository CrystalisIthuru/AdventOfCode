import aocd
import numpy as np
import re

def parse_input(input):

    sequences = []
    for line in input.split("\n"):
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

    sequences = parse_input(aocd.get_data(day = 9, year = 2023))

    print(sum([find_next_element(S) for S in sequences]))
    print(sum([find_previous_element(S) for S in sequences]))
