import aocd
import functools
import re

EXAMPLE = """
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
""".strip()

def find_optimal_seating(rules):

    def recurse(rules, seated, unseated, happiness):

        if len(unseated) == 0:
            return seated, happiness + rules[seated[0], seated[-1]] + rules[seated[-1], seated[0]]

        best_seating = None
        best_happiness = None
        for person in unseated:

            if not seated:
                current_happiness = 0
            else:
                current_happiness = happiness + rules[person, seated[-1]] + rules[seated[-1], person]

            next_seating, next_happiness = recurse(
                rules,
                seated + [person],
                unseated - set([person]),
                current_happiness,
            )

            if best_seating is None or next_happiness > best_happiness:
                best_seating = next_seating
                best_happiness = next_happiness

        return best_seating, best_happiness

    people = set(functools.reduce(lambda acc, x: acc + [x[0], x[1]], rules.keys(), []))
    return recurse(rules, [], people, 0)

if __name__ == "__main__":

    _in = EXAMPLE
    _in = aocd.get_data(year = 2015, day = 13)

    # Parse Input
    rules = {}
    for line in _in.split("\n"):
        match = re.match(r"(.*) would (gain|lose) (\d+) happiness units by sitting next to (.*).", line)
        
        if match.group(2) == "gain":
            rules[match.group(1), match.group(4)] = int(match.group(3))
        elif match.group(2) == "lose":
            rules[match.group(1), match.group(4)] = -int(match.group(3))
        else:
            raise Exception(f"Unknown term {match.group(2)}")
        
    # Part 1
    print(find_optimal_seating(rules)[1])

    # Part 2
    for person in set(functools.reduce(lambda acc, x: acc + [x[0], x[1]], rules.keys(), [])):
        rules["Me", person] = 0
        rules[person, "Me"] = 0
    print(find_optimal_seating(rules)[1])



