import aocd
import numpy as np
import re

EXAMPLE = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()

def is_okay(record):

    diffs = np.diff(record)

    if np.any(diffs == 0):
        return False

    if not np.all(diffs < 0) and not np.all(diffs > 0):
        return False
    
    return np.all(np.abs(diffs) <= 3)

if __name__ == "__main__":

    input = aocd.get_data(day = 2, year = 2024)

    # Parse Input
    A = []
    for line in input.split("\n"):
        line = line.strip()
        A += [[int(el) for el in re.findall(r"\d+", line)]]

    # Part 1
    safe_count = 0
    for record in A:
        if is_okay(record):
            safe_count += 1
    print(safe_count)

    # Part 2
    safe_count = 0
    for record in A:
        if is_okay(record):
            safe_count += 1
        else:
            for i in range(len(record)):
                if is_okay(record[:i] + record[i+1:]):
                    safe_count += 1
                    break
    print(safe_count)