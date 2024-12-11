import aocd
import functools

EXAMPLE = """
20
15
10
5
5
""".strip()

@functools.cache
def count_bucket_combos(buckets, target, combo = tuple()):

    if target == 0:
        return set([tuple(sorted(combo))])
    elif len(buckets) == 0:
        return set()
    
    combos = set()
    for i in range(len(buckets)):
        index, value = buckets[i]
        if value <= target and index not in combo:
            combos |= count_bucket_combos(buckets[:i] + buckets[i+1:], target - value, tuple(sorted(list(combo) + [index])))
    
    return combos
        

if __name__ == "__main__":

    _in = aocd.get_data(year = 2015, day = 17)

    # Parse Input
    buckets = tuple([(i, int(line.strip())) for i, line in enumerate(_in.split("\n"))])

    # Part 1
    combos = count_bucket_combos(buckets, 150)
    print(len(combos))

    # Part 2
    print(len([combo for combo in combos if len(combo) == min([len(combo) for combo in combos])]))