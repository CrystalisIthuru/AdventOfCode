import aocd
import functools
import re

EXAMPLE = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".strip()

def parseInput(_in):

    lines = [line.strip() for line in _in.split("\n") if line.strip()]
    components = [component.strip() for component in lines[0].split(",")]    
    targets = lines[1:]

    return components, targets


def build_towels(components, targets):

    @functools.cache
    def count_builds(target):

        if len(target) == 0:
            return 1
        
        count = 0
        for component in components:
            if target.startswith(component):
                count += count_builds(target[len(component):])

        return count

    count_possible = 0
    count_all_builds = 0
    for target in targets:
        count = count_builds(target)
        if count > 0:
            count_possible += 1
            count_all_builds += count

    return count_possible, count_all_builds

if __name__ == "__main__":

    _in = EXAMPLE
    _in = aocd.get_data(year = 2024, day = 19)

    # Parse Input
    components, targets = parseInput(_in)

    # Part 1 and 2
    print(*build_towels(components, targets))