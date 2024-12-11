import aocd
import numpy as np

EXAMPLE = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""".strip()

def get_block(A, loc):

    x, y = loc
    min_x = max(0, x - 1)
    min_y = max(0, y - 1)
    max_x = min(A.shape[0] - 1, x + 1)
    max_y = min(A.shape[1] - 1, y + 1)

    return A[min_x:max_x+1,min_y:max_y+1]

def run_lights(A, steps, stuck_corners = False):

    corners = [
        (0,                           0),
        (0,              A.shape[1] - 1),
        (A.shape[0] - 1,              0),
        (A.shape[0] - 1, A.shape[1] - 1)
    ]

    # Initialize
    current = np.copy(A)
    if stuck_corners:
        for x, y in corners:
            current[x, y] = "#"

    for _ in range(steps):

        state = np.copy(current)
        for idx, el in np.ndenumerate(current):

            if stuck_corners and idx in corners:
                continue
            
            block = get_block(current, idx)
            mask = np.where(block == "#", 1, 0)

            if el == "#":
                if np.sum(mask) - 1 in [2, 3]: # Subtract one for current position being on
                    state[*idx] = "#"
                else:
                    state[*idx] = "."
            else:
                if np.sum(mask) == 3:
                    state[*idx] = "#"
                else:
                    state[*idx] = "."

        current = state

    return current

if __name__ == "__main__":

    _in = aocd.get_data(year = 2015, day = 18)

    # Parse Input
    A = np.array([[char for char in line.strip()] for line in _in.split("\n")])

    # Part 1
    print(np.sum(np.where(run_lights(A, 100) == "#", 1, 0)))
    
    # Part 2
    print(np.sum(np.where(run_lights(A, 100, True) == "#", 1, 0)))
