import aocd
import functools
import numpy as np
import re

EXAMPLE = """
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
""".strip()

def find_best_combination(ingrediants, ingrediant_count, calorie_match = None):

    def find_all_partitions(elements, groups):

        if groups == 1:
            return [[elements]]

        partitions = []
        for i in range(elements + 1):
            partitions += [[i] + partition for partition in find_all_partitions(elements - i, groups - 1)]

        return partitions
    
    best_partition = None
    best_score = None
    for partition in find_all_partitions(ingrediant_count, len(ingrediants)):

        totals = [0, 0, 0, 0, 0]
        for i, count in enumerate(partition):
            for j in range(5):
                totals[j] += count * ingrediants[i][j + 1]

        if (calorie_match and calorie_match == totals[4]) or not calorie_match:
            score = functools.reduce(lambda acc, x: acc * x, [max(0, score) for score in totals[:4]], 1)
            if best_score is None or score > best_score:
                best_score = score
                best_partition = partition

    return best_partition, best_score

if __name__ == "__main__":

    _in = aocd.get_data(year = 2015, day = 15)

    # Parse Input
    ingrediants = []
    for line in _in.split("\n"):
        match = re.match(r"(.*): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)", line)
        ingrediants += [[match.group(1)] + [int(match.group(i)) for i in range(2, 7)]]

    # Part 1 
    print(find_best_combination(ingrediants, 100)[1])
    
    # Part 2
    print(find_best_combination(ingrediants, 100, 500)[1])