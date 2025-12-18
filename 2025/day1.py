import numpy as np

TEST = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

with open("day1.input") as f:
    INPUT = f.read()

def part1(input):

    dial = 50
    count = 0
    for line in input.strip().split():

        if line[0] == "L":
            dial -= int(line[1:])
        else:
            dial += int(line[1:])

        dial %= 100
        
        if dial == 0:
            count += 1
    
    return count

def part2(input):

    dial = 50
    count = 0
    for line in input.strip().split():

        prev = dial

        if line[0] == "L":
            dial -= int(line[1:])
        else:
            dial += int(line[1:])

        # Add one pass if the dial stops on zero or if
        # we crossed from positive numbers into negative
        if (prev > 0 and dial < 0) or dial == 0:
            count += 1

        # Add a count for every 100 dial values.
        count += int(np.abs(dial) / 100)
        
        # Normalize dial back to [0, 99]
        dial %= 100
    
    return count

if __name__ == "__main__":

    print(part1(INPUT))
    print(part2(INPUT))