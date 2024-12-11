import aocd
import numpy as np
import re
from functools import cache

EXAMPLE = "125 17"

@cache
def next_stone(stone):
    digits = len(str(stone))
    if stone == 0:
        return 1
    elif digits % 2 == 0:
        left = int(stone / (10 ** (digits // 2)))
        right = int(stone - (left * 10 ** (digits // 2)))
        return left, right
    else:
        return stone * 2024
    
@cache
def blink_stone(stone, blinks):

    if blinks == 0:
        return 1

    next_stones = next_stone(stone)
    if isinstance(next_stones, tuple):
        return blink_stones(next_stones, blinks - 1)
    else:
        return blink_stone(next_stones, blinks - 1)

@cache 
def blink_stones(stones, blinks):

    count = 0
    for stone in stones:
        count += blink_stone(stone, blinks)
    return count 

if __name__ == "__main__":

    _in = aocd.get_data(year = 2024, day = 11)

    # Parse Input
    stones = tuple([int(n) for n in re.findall(r"\d+", _in)])

    # Part 1
    print(blink_stones(stones, 25))
    
    # Part 2
    print(blink_stones(stones, 75))
