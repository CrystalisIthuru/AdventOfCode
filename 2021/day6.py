import aocd
import numpy as np

EXAMPLE = "3,4,3,1,2"

def simulate_fish(fish, days):

    fish_counts = [0 for _ in range(9)]
    for val, count in zip(*np.unique(fish, return_counts = True)):
        fish_counts[val] = int(count)

    for _ in range(days):
        
        # Add new fish and decrement all other fish
        new_fish = fish_counts.pop(0)
        fish_counts += [new_fish]

        # Update all fish with value zero to six
        fish_counts[6] += new_fish

    return fish_counts

if __name__ == "__main__":

#    input = EXAMPLE
    input = aocd.get_data(day = 6, year = 2021)
    fish = np.array([int(n) for n in input.strip().split(",")], dtype = int)

    # Part 1
    print(sum(simulate_fish(fish, 80)))

    # Part 2
    print(sum(simulate_fish(fish, 256)))
