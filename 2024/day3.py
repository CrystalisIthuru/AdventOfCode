import aocd
import re
import functools

EXAMPLE = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""".strip()

EXAMPLE2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""".strip()

if __name__ == "__main__":

    input = aocd.get_data(day = 3, year = 2024)

    # Part 1
    matches = [(int(x), int(y)) for x, y in re.findall(r"mul\((\d+),(\d+)\)", input)]
    print(functools.reduce(lambda acc, x: acc + x[0] * x[1], matches, 0))

    # Part 2
    matches = [m for m in re.findall(r"(?:mul\((\d+),(\d+)\)|(do)\(\)|(don't)\(\))", input)]
    acc = 0
    do = True
    for m in matches:
        if m[2] == "do":
            do = True
        elif m[3] == "don't":
            do = False
        else:
            if do:
                acc += int(m[0]) * int(m[1])
    print(acc)