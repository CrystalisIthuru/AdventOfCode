import aocd
import re
import functools

EXAMPLE = """
H => HO
H => OH
O => HH

HOH
"""

EXAMPLE2 = """
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
"""

def count_calibration(rules, start):

    molicules = set()
    for left, replacements in rules.items():
        for replacement in replacements:
            for match in re.finditer(left, start):
                molicule = start[:match.start()] + replacement + start[match.end():]
                molicules.add(molicule)

    return len(molicules)

# Super greedy, like OMG greedy. I should get coal for christmas
# greedy. Assume that only the replacement for the largest matching
# rule applies. Who needs a search.
def count_molicule_fabrication(rules, target):

    def invert_rules(rules):
        d = {}
        for k, vs in rules.items():
            for v in vs:
                if v in d:
                    raise Exception()
                else:
                    d[v] = k
        return d

    @functools.cache
    def recur(current):

        if current == "e":
            return 0

        largest = ""
        for molicule in rules.keys():
            if molicule in current and (largest is None or len(molicule) > len(largest)):
                largest = molicule

        match = re.search(largest, current)
        next = current[:match.start()] + rules[largest] + current[match.end():]
        return recur(next) + 1
    
    rules = invert_rules(rules)
    return recur(target)        

if __name__ == "__main__":

    _in = aocd.get_data(year = 2015, day = 19)
    
    # Parse Input
    rules = {}
    start = ""
    for line in _in.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        match = re.match(r"(.*) => (.*)", line)
        if match:
            if match.group(1) not in rules:
                rules[match.group(1)] = []
            rules[match.group(1)] += [match.group(2)]
        else:
            start = line

# Part 1
print(count_calibration(rules, start))

# Part 2
print(count_molicule_fabrication(rules, start))