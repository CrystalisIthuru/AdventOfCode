import aocd
import numpy as np
import enum
import copy

EXAMPLE = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()

class Move(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

MOVEMENTS = {
    Move.UP    : np.array((-1,  0)),
    Move.LEFT  : np.array(( 0, -1)),
    Move.RIGHT : np.array(( 0,  1)),
    Move.DOWN  : np.array(( 1,  0))
}

def find_start_position(A):

    movements = {
        ">" : Move.RIGHT,
        "<" : Move.LEFT,
        "^" : Move.UP,
        "v" : Move.DOWN
    }
    
    for symbol in movements.keys():
         if np.any(A == symbol):
            return np.argwhere(A == symbol)[0,:], movements[symbol]
        
def find_obstacles(A):

    obstacles = np.argwhere(A == "#")
    obstacles = set([(obstacles[i,0], obstacles[i,1]) for i in range(obstacles.shape[0])])
    return obstacles

def move_guard(guard_start, direction_start, obstacles, shape):

    guard = guard_start
    direction = direction_start
    visited_list = [(*guard_start, direction_start)]
    visited_set = set(visited_list)
    while True:

        x, y = guard + MOVEMENTS[direction]

        # Stop if off board
        if x < 0 or x >= shape[0] or y < 0 or y >= shape[1]:
            break
        
        # Change direction if hit obstacle
        if (x, y) in obstacles:
            direction = Move((direction.value + 1) % 4)
            continue

        # Stop if in cycle
        if (x, y, direction) in visited_set:
            return visited_list, True

        guard = (x, y)
        visited_list += [(x, y, direction)]
        visited_set.add((x, y, direction))

    return visited_list, False

def check_for_cycles(start, start_direction, visited, obstacles, shape):

    obstacle_set = set()
    for i, (x, y, direction) in enumerate(visited):

        new_obstacle = (x, y)

        if all(start == new_obstacle):
            continue

        new_obstacles = copy.deepcopy(obstacles)
        new_obstacles.add(new_obstacle)

        _, cycle = move_guard(start, start_direction, new_obstacles, shape)
        if cycle:
            obstacle_set.add(new_obstacle)
    
    return len(obstacle_set)

def visualize_path(obstacles, visited, shape):

    A = np.full(shape, ".")
    for x, y in obstacles:
        A[x, y] = "#"
    
    for i, (x, y, direction) in enumerate(visited):

        if i == 0:
            A[x,y] = "&"
        elif i == len(visited) - 1:
            A[x,y] = "!"
        else:
            A[x,y] = "X"

    return A

if __name__ == "__main__":

    _input = aocd.get_data(day = 6, year = 2024)
    A = np.array([[char for char in line.strip()] for line in _input.split("\n")])

    guard_start, direction_start = find_start_position(A)
    obstacles = find_obstacles(A)
    visited, _ = move_guard(guard_start, direction_start, obstacles, A.shape)

    # Part 1
    positions = set()
    for x, y, direction in visited:
        positions.add((x, y))
    print(len(positions))

    # Part 2
    print(check_for_cycles(guard_start, direction_start, visited, obstacles, A.shape))