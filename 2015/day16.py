import aocd
import re

GIFT = {
    "children" : 3,
    "cats" : 7,
    "samoyeds" : 2,
    "pomeranians" : 3,
    "akitas" : 0,
    "vizslas" : 0,
    "goldfish" : 5,
    "trees" : 3,
    "cars" : 2,
    "perfumes" : 1
}

def filter_aunts(aunts, retroencabulator_fix = False):

    for key, value in GIFT.items():
        
        comp_func = lambda aunt: key not in aunt or aunt[key] == value
        if retroencabulator_fix and key in ["cats", "trees"]:
            comp_func = lambda aunt: key not in aunt or aunt[key] > value
        elif retroencabulator_fix and key in ["pimeranians", "goldfish"]:
            comp_func = lambda aunt: key not in aunt or aunt[key] < value
        
        aunts = list(filter(comp_func, aunts))
    
    return aunts

if __name__ == "__main__":

    _in = aocd.get_data(year = 2015, day = 16)

    # Parse Input
    aunts  = []
    for line in _in.split("\n"):
        line = line.strip()
        match = re.match(r"Sue (\d+): ([a-zA-Z]*): (\d+), ([a-zA-Z]*): (\d+), ([a-zA-Z]*): (\d+)", line)
        elements = match.groups()
        sue = { "id" : int(elements[0]) }
        for i in range(1, len(elements), 2):
            sue[elements[i]] = int(elements[i + 1])
        aunts += [sue]

    # Part 1
    print(filter_aunts(aunts)[0]["id"])
    
    # Part 2
    print(filter_aunts(aunts, True)[0]["id"])