import aocd
import enum
import re

EXAMPLE = """
A Y
B X
C Z
""".strip()

class RPS(enum.Enum):

    ROCK = 1
    PAPER = 2
    SCISSORS = 3

ELF_CONVERSION = {
    "A" : RPS.ROCK,
    "B" : RPS.PAPER,
    "C" : RPS.SCISSORS
}

MY_CONVERSION = {
    "X" : RPS.ROCK,
    "Y" : RPS.PAPER,
    "Z" : RPS.SCISSORS
}

OUTCOME_CONVERSION = {
    "X" : "loss",
    "Y" : "draw",
    "Z" : "win"
}

def roshambo(left, right):

    game = {
        (RPS.ROCK, RPS.ROCK)         : "draw",
        (RPS.ROCK, RPS.PAPER)        : "win",
        (RPS.ROCK, RPS.SCISSORS)     : "loss",
        (RPS.PAPER, RPS.ROCK)        : "loss",
        (RPS.PAPER, RPS.PAPER)       : "draw",
        (RPS.PAPER, RPS.SCISSORS)    : "win",
        (RPS.SCISSORS, RPS.ROCK)     : "win",
        (RPS.SCISSORS, RPS.PAPER)    : "loss",
        (RPS.SCISSORS, RPS.SCISSORS) : "draw",
    }

    return game[left, right]

def roshambo_fix (left, outcome):

    game = {
        (RPS.ROCK, "win")      : RPS.PAPER,
        (RPS.ROCK, "draw")     : RPS.ROCK,
        (RPS.ROCK, "loss")     : RPS.SCISSORS,
        (RPS.SCISSORS, "win")  : RPS.ROCK,
        (RPS.SCISSORS, "draw") : RPS.SCISSORS,
        (RPS.SCISSORS, "loss") : RPS.PAPER,
        (RPS.PAPER, "win")     : RPS.SCISSORS,
        (RPS.PAPER, "draw")    : RPS.PAPER,
        (RPS.PAPER, "loss")    : RPS.ROCK,
    }

    return game[left, outcome]

def score(outcome, hand):

    if outcome == "loss":
        return 0 + hand.value
    elif outcome == "draw":
        return 3 + hand.value
    elif outcome == "win":
        return 6 + hand.value

if __name__ == "__main__":

    input = aocd.get_data(day = 2, year = 2022)
#    input = EXAMPLE

    guide = []
    for line in input.split("\n"):
        line = line.strip()
        guide += [re.split(r"\s+", line)]
    
    # Part 1
    print(sum([score(roshambo(ELF_CONVERSION[left], MY_CONVERSION[right]), MY_CONVERSION[right]) for left, right in guide]))

    # Part 2
    print(sum([score(OUTCOME_CONVERSION[right], roshambo_fix(ELF_CONVERSION[left], OUTCOME_CONVERSION[right])) for left, right in guide]))