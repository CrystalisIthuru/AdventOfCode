import aocd
import numpy as np

EXAMPLE = """
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
""".strip()

EXAMPLE2 = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()

EXAMPLE3 = """
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
""".strip()

def count_hiking_trails(map, use_rating = False):

    def walk_trail(map, position, stop_elevation):

        if map[*position] == stop_elevation:
            return set([tuple(position)])

        movements = [
            np.array([-1,  0]), # Up
            np.array([ 1,  0]), # Down
            np.array([ 0, -1]), # Left
            np.array([ 0,  1])  # Right
        ]
        
        peaks = set()
        for movement in movements:

            next = position + movement
            x, y = next

            if x < 0 or x >= map.shape[0] or y < 0 or y >= map.shape[1]:
                continue

            if map[*position] + 1 == map[x, y]:
                peaks = peaks | walk_trail(map, next, stop_elevation)
        
        return peaks
    
    def walk_trail_rating(map, position, stop_elevation):
        
        if map[*position] == stop_elevation:
            return 1

        movements = [
            np.array([-1,  0]), # Up
            np.array([ 1,  0]), # Down
            np.array([ 0, -1]), # Left
            np.array([ 0,  1])  # Right
        ]
        
        count = 0
        for movement in movements:

            next = position + movement
            x, y = next

            if x < 0 or x >= map.shape[0] or y < 0 or y >= map.shape[1]:
                continue

            if map[*position] + 1 == map[x, y]:
                count += walk_trail_rating(map, next, stop_elevation)
        
        return count


    trailheads = np.argwhere(map == 0)
    result = 0
    for i in range(trailheads.shape[0]):
        if use_rating:
            result += walk_trail_rating(map, trailheads[i,:], 9)
        else:
            result += len(walk_trail(map, trailheads[i,:], 9))
    
    return result

if __name__ == "__main__":

    _in = aocd.get_data(year = 2024, day = 10)

    # Parse Input
    map = np.array([[-1 if char == "." else int(char) for char in line.strip()] for line in _in.split("\n")])
    
    # Part 1
    print(count_hiking_trails(map))

    # Part 2
    print(count_hiking_trails(map, True))