import aocd
import numpy as np
import re
import functools

EXAMPLE = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()

PART1_OPERATORS = [lambda x, y: x + y, lambda x, y: x * y]
PART2_OPERATORS = [lambda x, y: x + y, lambda x, y: x * y, lambda x, y: int(str(x) + str(y))]

def is_true_equation(test_value, operands, operators):

    def recurse(test_value, operands, operators, current_value):
        if not operands:
            return current_value == test_value
        else:
            return functools.reduce(
                lambda acc, x: acc or recurse(
                    test_value,
                    operands[1:],
                    operators,
                    x(current_value, operands[0])
                ),
                operators,
                False
            )
    
    return recurse(test_value, operands[1:], operators, operands[0])

if __name__ == "__main__":

    _in = EXAMPLE
    _in = aocd.get_data(year = 2024, day = 7)

    # Parse Input
    equations = []
    for line in _in.split("\n"):
        numbers = [int(n) for n in re.findall(r"\d+", line)]
        equations += [(numbers[0], numbers[1:])]

    # Part 1 
    print(sum([test_value for test_value, operands in equations if is_true_equation(test_value, operands, PART1_OPERATORS)]))
    
    # Part 2 
    print(sum([test_value for test_value, operands in equations if is_true_equation(test_value, operands, PART2_OPERATORS)]))
