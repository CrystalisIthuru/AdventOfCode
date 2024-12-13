import aocd
import functools
import numpy as np
import re

EXAMPLE = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip()

class ClawGame:

    def __init__(self, button_a, button_b, prize):

        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize

def run_game(game):

    # Just do linear algebra, solve Ax = b

    A = np.array([
        [game.button_a[0], game.button_b[0]],
        [game.button_a[1], game.button_b[1]]
    ], dtype = int)

    a, b, c, d = game.button_a[0], game.button_b[0], game.button_a[1], game.button_b[1]
    x, y = game.prize[0], game.prize[1]

    det = 1 / ((a * d) - (b * c))

    _x = int(np.round(det * (d * x - b * y)))
    _y = int(np.round(det * (-c * x + a * y)))

    loc = game.button_a[0] * _x + game.button_b[0] * _y, game.button_a[1] * _x + game.button_b[1] * _y

    if loc == game.prize:
        return _x, _y
    else:
        return None

if __name__ == "__main__":

    _in = aocd.get_data(year = 2024, day = 13)

    # Parse Input
    games = []
    lines = [line.strip() for line in _in.split("\n") if line.strip()]
    for i in range(0, len(lines), 3):

        games += [ClawGame(
            tuple([int(n) for n in re.findall(r"\d+", lines[i])]),
            tuple([int(n) for n in re.findall(r"\d+", lines[i+1])]),
            tuple([int(n) for n in re.findall(r"\d+", lines[i+2])])
        )]

    # Part 1
    moves = [run_game(game) for game in games]
    print(sum(map(lambda x: x[0] * 3 + x[1] if x is not None else 0, moves)))

    # Part 2
    for game in games:
        game.prize = game.prize[0] + 10000000000000, game.prize[1] + 10000000000000
    
    moves = [run_game(game) for game in games]
    print(sum(map(lambda x: x[0] * 3 + x[1] if x is not None else 0, moves)))