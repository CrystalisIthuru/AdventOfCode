import aocd
import functools
import numpy as np

EXAMPLE = """
1
10
100
2024
""".strip()

EXAMPLE2 = """
1
2
3
2024
""".strip()

@functools.cache
def mix(value, secret):
    return value ^ secret

@functools.cache
def prune(secret):
    return secret % 16777216

@functools.cache
def evolve(secret):

    secret = prune(mix(secret << 6, secret))
    secret = prune(mix(int(secret >> 5), secret))
    secret = prune(mix(secret << 11, secret))

    return secret

if __name__ == "__main__":

    _in = aocd.get_data(year = 2024, day = 22)

    # Parse Input
    secrets = [int(n) for n in _in.split("\n")]

    # Calculate all secret numbers
    secrets = { n : [n] for n in secrets}
    for secret in secrets.keys():
        current = secret
        for _ in range(2000):
            current = evolve(current)
            secrets[secret] += [current]

    # Calculates the value associated with each sequence of four price
    # changes. Tag them by the starting secret number to keep them 
    # separate. We need to keep them separate because for each secret
    # number a sequence can only be value for the first iteration it
    # exists. 
    sequences = {}
    for start, numbers in secrets.items():

        prices = [n % 10 for n in numbers]
        diffs = [int(n) for n in np.diff(prices)]

        for i in range(3, len(diffs)):
            sequence = (diffs[i - 3], diffs[i - 2], diffs[i - 1], diffs[i])
            
            if (start, sequence) in sequences:
                continue
            else:
                sequences[start, sequence] = prices[i + 1]

    # Merge all the sequences and values together across each
    # secret number start.
    merged = {}
    for (_, sequence), value in sequences.items():
        if sequence not in merged:
            merged[sequence] = value
        else:
            merged[sequence] += value

    # Find the sequences with the largest value
    best_value = None
    best_sequence = None
    for sequence, value in merged.items():
        if best_value is None or value > best_value:
            best_sequence = sequence
            best_value = value

    # Part 1
    print(sum([v[-1] for k, v in secrets.items()]))

    # Part 2
    print(best_value)