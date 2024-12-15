import aocd
import numpy as np

EXAMPLE = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""".strip()

EXAMPLE2 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()

EXAMPLE3 = """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
""".strip()

def move_robot(map, allmoves):
        
    movements = {
        "^" : np.array([-1, 0]),
        ">" : np.array([0, 1]),
        "v" : np.array([1, 0]),
        "<" : np.array([0, -1])
    }

    def can_move(loc, move):

        maybe = loc + movements[move]
        symbol = map[*maybe]

        if symbol == "O":
            return can_move(maybe, move)
        elif symbol == "#":
            return False
        elif symbol == "[":
            if move in "^v":
                right = maybe + np.array([0, 1])
                return can_move(maybe, move) and can_move(right, move)
            else:
                return can_move(maybe, move)
        elif symbol == "]":
            if move in "^v":
                left = maybe + np.array([0, -1])
                return can_move(maybe, move) and can_move(left, move)
            else:
                return can_move(maybe, move)
        elif symbol == ".":
            return True

    def single_move(loc, move):

        maybe = loc + movements[move]
        symbol = map[*maybe]

        if symbol == "O":
            single_move(maybe, move)
            map[*maybe] = map[*loc]
            map[*loc] = "."
        elif symbol == ".":
            map[*maybe] = map[*loc]
            map[*loc] = "."
        elif symbol == "[":
            if move in "^v":
                right = maybe + np.array([0, 1])
                single_move(maybe, move)
                single_move(right, move)
            else:
                single_move(maybe, move)
            map[*maybe] = map[*loc]
            map[*loc] = "."
        elif symbol == "]":
            if move in "^v":
                left = maybe + np.array([0, -1])
                single_move(maybe, move)
                single_move(left, move)
            else:
                single_move(maybe, move)
            map[*maybe] = map[*loc]
            map[*loc] = "."
        else:
            raise Exception("Unknown symbol " + symbol)

    for move in allmoves:
        loc = np.argwhere(map == "@")[0,:]
        if can_move(loc, move):
            single_move(loc, move)
    
    return map
        
def score_gps(map):

    score = 0
    boxes = np.argwhere(np.logical_or(map == "O", map == "["))
    for i in range(boxes.shape[0]):
        x, y = boxes[i,:]
        score += 100 * x + y
    
    return score

def parseInput(_in, doublemap = False):
    
    map = []
    movements = ""
    parsing_map = True
    for line in _in.split("\n"):
        line = line.strip()

        if not line:
            parsing_map = False
        elif parsing_map:
            row = []
            for char in line:
                if doublemap:
                    if char == "O":
                        row += ["[", "]"]
                    elif char == "@":
                        row += ["@", "."]
                    else:
                        row += [char] * 2
                else:
                    row += [char]
            map += [row]
        else:
            movements += line
    map = np.array(map)
    return map, movements

if __name__ == "__main__":

    _in = EXAMPLE2
    _in = aocd.get_data(year = 2024, day = 15)

    # Part 1
    map, movements = parseInput(_in)
    print(score_gps(move_robot(np.copy(map), movements)))

    # Part 2
    map, movements = parseInput(_in, True)
    print(score_gps(move_robot(np.copy(map), movements)))
