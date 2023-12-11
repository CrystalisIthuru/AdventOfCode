from functools import reduce
import numpy as np
import os
import re

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "11.dat")

def expand_universe(universe):

    expanded_rows = []
    for r in range(universe.shape[0]):
        if np.all(universe[r,:] == "."):
            expanded_rows += [r]

    expanded_cols = []
    for c in range(universe.shape[1]):
        if np.all(universe[:,c] == "."):
            expanded_cols += [c]

    return expanded_rows, expanded_cols

def find_galaxy_pairs(universe):

    galaxies = np.argwhere(universe == "#")

    pairs = []
    for i in range(galaxies.shape[0]):
        for j in range(i + 1, galaxies.shape[0]):
            pairs += [(galaxies[i,:], galaxies[j,:])]

    return pairs

def manhattan_distance(left, right, expanded_rows = [], expanded_cols = [], expand_size = 1):

    distance = np.sum(np.abs(left - right))

    for r in expanded_rows:
        if left[0] <= right[0] and left[0] <= r <= right[0]:
            distance += expand_size - 1
        elif left[0] > right[0] and right[0] <= r <= left[1]:
            distance += expand_size - 1
    
    for c in expanded_cols:
        if left[1] <= right[1] and left[1] <= c <= right[1]:
            distance += expand_size - 1
        elif left[1] > right[1] and right[1] <= c <= left[1]:
            distance += expand_size - 1

    return distance

def parse_input(input_file):

    with open(input_file, "r") as f:
        lines = f.readlines()

    return np.array([re.split("", line.strip())[1:-1] for line in lines])

if __name__ == "__main__":

    universe = parse_input(INPUT_FILE)

    expanded_rows, expanded_cols = expand_universe(universe)
    galaxy_pairs = find_galaxy_pairs(universe)
    print(reduce(lambda acc, x: acc + manhattan_distance(*x, expanded_rows, expanded_cols, 2), galaxy_pairs, 0))
    print(reduce(lambda acc, x: acc + manhattan_distance(*x, expanded_rows, expanded_cols, 1000000), galaxy_pairs, 0))


