import aocd
import numpy as np
import re

EXAMPLE = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

def map_vents(vents, consider_diagonal = False):

    max_x = max(np.max(vents[:,0]), np.max(vents[:,2]))
    max_y = max(np.max(vents[:,1]), np.max(vents[:,3]))

    seabed = np.zeros((max_y + 1, max_x + 1), dtype = int)

    for i in range(vents.shape[0]):
        x1, y1, x2, y2 = vents[i,:]

        # Only consider horizontal and vertical lines
        if x1 == x2 or y1 == y2:

            x1 = min(vents[i,0], vents[i,2])
            x2 = max(vents[i,0], vents[i,2])
            y1 = min(vents[i,1], vents[i,3])
            y2 = max(vents[i,1], vents[i,3])

            seabed[y1:y2+1,x1:x2+1] += 1
        elif consider_diagonal:

            xmove = 1 if x2 - x1 > 0 else -1
            ymove = 1 if y2 - y1 > 0 else -1

            x, y = x1, y1
            while x != x2 and y != y2:
                seabed[y, x] += 1
                x = x + xmove
                y = y + ymove            
            seabed[y, x] += 1

    return seabed

def score_map(map):
    return np.sum(np.where(map > 1, 1, 0))

if __name__ == "__main__":

    input = EXAMPLE
    input = aocd.get_data(day = 5, year = 2021)

    # Parse Input
    vents = []
    for line in [line.strip() for line in input.split("\n")]:
        match = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line)
        if match:
            vents += [[int(x) for x in match.group(1, 2, 3, 4)]]
    vents = np.array(vents)

    # Part 1
    print(score_map(map_vents(vents)))

    # Part 2
    print(score_map(map_vents(vents, True)))
