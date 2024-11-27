import aocd
import numpy as np

EXAMPLE_SMALL = """
11111
19991
19191
19991
11111
""".strip()

EXAMPLE = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".strip()

def step(A):

    # Increase Energy
    A += 1

    # Find all octipi about to flash
    flashed = np.zeros_like(A, dtype = bool)
    flashing = np.where(A > 9, True, False)
    while np.any(np.logical_and(flashing, np.logical_not(flashed))):

        # Current Flashing
        x, y = np.argwhere(np.logical_and(flashing, np.logical_not(flashed)))[0,:]

        # Single Flash
        min_x = max(x - 1, 0)
        max_x = min(x + 1, A.shape[0] - 1)
        min_y = max(y - 1, 0)
        max_y = min(y + 1, A.shape[1] - 1)

        A[min_x:max_x + 1, min_y:max_y + 1] += 1

        # Update Tracking
        flashing = np.logical_or(flashing, A > 9)
        flashed[x, y] = True

    A[flashed] = 0

    return A, int(np.sum(flashed))

def run_steps(A, steps):

    A_copy = np.copy(A)
    flash_count = 0 
    for _ in range(steps):
        A_copy, flashes = step(A_copy)
        flash_count += flashes
    
    return A_copy, flash_count

def find_synchronization(A):

    A_ = np.copy(A)
    count = 0
    while np.any(A_ != 0):
        A_, _ = step(A_)
        count += 1
    
    return count

if __name__ == "__main__":

    problem_input = aocd.get_data(day = 11, year = 2021)
    A = np.array([[int(char) for char in line.strip()] for line in problem_input.split("\n")])

    # Part 1
    print(run_steps(A, 100)[1])

    # Part 2
    print(find_synchronization(A))