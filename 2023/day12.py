from functools import reduce, cache
import numpy as np
import os
import re

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "12.dat")

def parse_input(input_file, unfold = 1):

    nonograms = []

    with open(input_file, "r") as f:
        for line in f:
            if line.strip() == "": continue
            match = re.match(r"([\?\.#]+)\s((?:\d+,?)+)", line)

            nonogram = "?".join([match.group(1)] * unfold)
            clues = ",".join([match.group(2)] * unfold)

            nonograms += [(nonogram, clues)]

    return nonograms

@cache
def count_nonogram_solutions(nonogram, clues):

    if len(clues) == 0:
        if len(nonogram) == 0 or reduce(lambda acc, char: acc and char != "#", nonogram, True):
            return 1
        else:
            return 0

    clues = list(map(int, clues.split(",")))

    nonogram_min_length = sum(clues) + len(clues) - 1
    shift = abs(nonogram_min_length - len(nonogram))

    clue = clues[0]

    if shift == 0:

        block_valid = reduce(lambda acc, char: acc and char != ".", nonogram[:clue], True)
        next_space_valid = len(nonogram) == clue or (len(nonogram) > clue and nonogram[clue] in [".", "?"])

        if block_valid and next_space_valid:
            return count_nonogram_solutions(nonogram[clue + 1:], ",".join(map(str, clues[1:])))
        else:
            return 0
    else:

        solution_count = 0
        for i in range(shift + 1):
            
            prev_space_valid = reduce(lambda acc, char: acc and char != "#", nonogram[:i], True)
            block_valid = reduce(lambda acc, char: acc and char != ".", nonogram[i:i + clue], True)
            next_space_valid = len(nonogram) <= i + clue or nonogram[i + clue] in [".", "?"] 

            if block_valid and next_space_valid and prev_space_valid:
                solution_count += count_nonogram_solutions(nonogram[i + clue + 1:], ",".join(map(str, clues[1:])))

        return solution_count

if __name__ == "__main__":

    part1_nonograms = parse_input(INPUT_FILE)
    part2_nonograms = parse_input(INPUT_FILE, 5)

    print(reduce(lambda acc, x: acc + count_nonogram_solutions(*x), part1_nonograms, 0))
    print(reduce(lambda acc, x: acc + count_nonogram_solutions(*x), part2_nonograms, 0))