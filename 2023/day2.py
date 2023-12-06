import re
import os
import functools

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "2.dat")

scanner = re.Scanner([
    (r"Game \d+:", lambda s, t: ("GAME", int(re.search(r"(\d+)", t).group(1)))),
    (r"\d+ red", lambda s, t: ("RED", int(re.search(r"(\d+)", t).group(1)))),
    (r"\d+ blue", lambda s, t: ("BLUE", int(re.search(r"(\d+)", t).group(1)))),
    (r"\d+ green", lambda s, t: ("GREEN", int(re.search(r"(\d+)", t).group(1)))),
    #(r",", lambda s, t: "HAND-END"),
    (r",", None),
    (r";", lambda s, t: ("ROUND-END", None)),
    (r"\s+", None)
])

RED_TOTAL = 12
GREEN_TOTAL = 13
BLUE_TOTAL = 14

COLOR_TOTALS = {
    "RED" : 12,
    "GREEN" : 13,
    "BLUE" : 14
}

possible_games = []
all_color_minimums = []
with open(INPUT_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if len(line) == 0: continue

        tokens, _ = scanner.scan(line)
        _, game_id = tokens[0]

        color_minimums = {
            "RED" : 0,
            "GREEN" : 0,
            "BLUE" : 0
        }

        possible_game = True

        for token_type, token_value in tokens[1:]:
            if token_type == "ROUND-END": continue

            if color_minimums[token_type] < token_value:
                color_minimums[token_type] = token_value

            if token_value > COLOR_TOTALS[token_type]:
                possible_game = False

        all_color_minimums += [color_minimums] 
        if possible_game: possible_games += [game_id]


print(possible_games)
print(sum(possible_games))


#from pprint import pprint
#pprint(all_color_minimums)
print(sum([functools.reduce(lambda acc, x: acc * x, color_minimums.values(), 1) for color_minimums in all_color_minimums]))


