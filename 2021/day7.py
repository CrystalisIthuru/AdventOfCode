import aocd
import numpy as np

EXAMPLE = "16,1,2,0,4,2,7,1,2,14"

def determineMostFuelEffiencientMove(crabs, part1 = True):

    cost = np.zeros_like(crabs, dtype = int)
    for i in range(crabs.size):
        for j in range(crabs.size):
            if part1:
                cost[i] += np.abs(crabs[j] - i)
            else:
                n = np.abs(crabs[j] - i)
                cost[i] += (n * (n + 1)) / 2
    

    return np.min(cost)

if __name__ == "__main__":

    input = EXAMPLE
    input = aocd.get_data(day = 7, year =  2021)
    crabs = np.array([int(n) for n in input.strip().split(",")])

    # Part 1
    print(determineMostFuelEffiencientMove(crabs))

    # Part 2
    print(determineMostFuelEffiencientMove(crabs, False))