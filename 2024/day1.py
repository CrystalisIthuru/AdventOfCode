import aocd
import re
import numpy as np

EXAMPLE = """
3   4
4   3
2   5
1   3
3   9
3   3
""".strip()

if __name__ == "__main__":

    input = aocd.get_data(day = 1, year = 2024)
    #input = EXAMPLE

    numbers = [int(el) for el in re.findall(r"\d+", input)]

    # Part 1
    list1 = np.array(sorted(numbers[::2]))
    list2 = np.array(sorted(numbers[1::2]))
    print(np.sum(np.abs(list2 - list1)))

    # Part 2
    list1 = np.array(numbers[::2])
    list2 = np.array(numbers[1::2])
    mapping = { el : count for el, count in zip(*np.unique(list2, return_counts = True)) }

    count = 0
    for el in list1:
        if el in mapping:
            count += el * mapping[el]
    print(count)
