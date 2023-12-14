import os
import numpy as np
from functools import cache

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "14.dat")

def parse_input(input_file):

    with open(input_file, "r") as f:
        data = f.read()

    return data

def find_tilt_distance(dish, rock_location):

    i, j = rock_location
    rock_row = dish[:i, j]

    if rock_row.size == 0: return 0
    block_locations = np.argwhere(rock_row != ".")

    if block_locations.size != 0:
        return rock_row.size - (block_locations[-1, 0] + 1)
    else:
        return rock_row.size

@cache
def tilt(dish):
            
    dish = np.array([[char for char in line] for line in dish.split("\n")])

    rock_locations = np.argwhere(dish == "O")
    for rock_index in range(rock_locations.shape[0]):
        i, j = rock_locations[rock_index,:]
        tilt_distance = find_tilt_distance(dish, (i, j))

        if tilt_distance != 0:
            dish[i - tilt_distance, j] = "O"
            dish[i, j] = "."

    dish = "\n".join(["".join(dish[i,:]) for i in range(dish.shape[0])])
    return dish

@cache
def calculate_total_load(dish):
    
    dish = np.array([[char for char in line] for line in dish.split("\n")]) 
    locations = np.argwhere(dish == "O")
    return sum(map(lambda x: dish.shape[0] - x, locations[:,0]))

def one_spin_cycle(dish):
        
    for i in range(4):
        dish = tilt(dish)
        dish = np.array([[char for char in line] for line in dish.split("\n")])
        dish = np.rot90(dish, 3)
        dish = "\n".join(["".join(dish[i,:]) for i in range(dish.shape[0])])
    return dish

def find_cycle(dish, cycles):

    all_cycles = {hash(dish) : 0 }
    for i in range(1, cycles + 1):
        dish = one_spin_cycle(dish)
        if hash(dish) in all_cycles:
            cycle_length = i - all_cycles[hash(dish)]
            non_cycle_length = i - cycle_length
            return dish, cycle_length, non_cycle_length
        else:
            all_cycles[hash(dish)] = i
    else:
        return None, None, None

def spin_cycle(dish, cycles):

    dish, cycle_length, non_cycle_length = find_cycle(dish, cycles)

    steps = (cycles - non_cycle_length) % cycle_length
    for _ in range(steps):
        dish = one_spin_cycle(dish)

    return calculate_total_load(dish)

if __name__ == "__main__":

    # Not my best work. Slow. Probably all the turning string to array and back

    dish = parse_input(INPUT_FILE)
    print(calculate_total_load(tilt(dish)))
    
    dish = parse_input(INPUT_FILE)    
    print(spin_cycle(dish, 1000000000))
