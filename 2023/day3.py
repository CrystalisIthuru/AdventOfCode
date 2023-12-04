import os
import numpy as np

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "3.dat")

def parse_input(input_file):

    with open(input_file, "r") as f:
        data = f.read()

    lines = data.split()
    input = np.zeros((len(lines), len(lines[0])), dtype = str)

    for i, line in enumerate(lines):
        input[i,:] = [s for s in line]

    return input

def find_part_numbers(input):

    non_symbol_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]

    part_numbers = []
    current_number = ""
    is_part_number = False
    for (i, j), char in np.ndenumerate(input):
        if char.isdigit():
            current_number += char

            lower_bound_i = max(i - 1, 0)
            lower_bound_j = max(j - 1, 0)

            window = input[lower_bound_i:i+2, lower_bound_j:j+2]
            mask = np.ones(window.shape, dtype = bool)
            
            for symbol in non_symbol_characters:
                mask = np.logical_and(mask, window != symbol)

            if np.any(mask): is_part_number = True

        else:
            if is_part_number:
                part_numbers += [int(current_number)]

            current_number = ""
            is_part_number = False

    return part_numbers

def find_gear_ratios(input):

    non_symbol_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    input_indices = np.indices(input.shape)

    symbols = {}
    current_number = ""
    associated_symbols = set()
    for (i, j), char in np.ndenumerate(input):
        if char.isdigit():
            current_number += char

            lower_bound_i = max(i - 1, 0)
            lower_bound_j = max(j - 1, 0)

            window = input[lower_bound_i:i+2, lower_bound_j:j+2]
            window_indices = input_indices[:,lower_bound_i:i+2,lower_bound_j:j+2]
            mask = np.ones(window.shape, dtype = bool)
            
            for symbol in non_symbol_characters:
                mask = np.logical_and(mask, window != symbol)

            symbol_indices = np.argwhere(mask)
            symbol_indices = window_indices[:, symbol_indices[:,0], symbol_indices[:,1]]
            for i in range(symbol_indices.shape[1]):
                associated_symbols.add(tuple(symbol_indices[:,i]))

        else:
            if len(associated_symbols) > 0:
                for associated_symbol in associated_symbols:
                    if associated_symbol not in symbols:
                        symbols[associated_symbol] = []
                    symbols[associated_symbol] += [int(current_number)]

            current_number = ""
            associated_symbols = set()

    gear_ratios = []
    for key, value in symbols.items():
        if len(value) == 2:
            gear_ratios += [value[0] * value[1]]

    return gear_ratios

if __name__ == "__main__":

    input = parse_input(INPUT_FILE)
    part_numbers = find_part_numbers(input)
    print(sum(part_numbers))

    gear_ratios = find_gear_ratios(input)
    print(sum(gear_ratios))
