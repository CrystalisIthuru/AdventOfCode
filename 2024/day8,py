import aocd
import numpy as np

EXAMPLE = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()

EXAMPLE2 = """
..........
..........
..........
....a.....
..........
.....a....
..........
..........
..........
..........
""".strip()

EXAMPLE3 = """
T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........
""".strip()

def find_antinodes(A, only_surrounding = True):

    def inbounds(shape, x, y):
        return not (x < 0 or x >= shape[0] or y < 0 or y >= shape[1])

    antennas = np.unique(A)
    antennas = np.delete(antennas, np.argwhere(antennas == ".")[0])

    antinodes = np.zeros_like(A, dtype = bool)
    for antenna in antennas:

        positions = np.argwhere(A == antenna)

        for i in range(positions.shape[0]):
            for j in range(i + 1, positions.shape[0]):

                a1 = positions[i,:]
                a2 = positions[j,:]
                diff = a2 - a1

                if only_surrounding:

                    x1, y1 = a1 - diff
                    x2, y2 = a2 + diff

                    if inbounds(A.shape, x1, y1):
                        antinodes[x1, y1] = True
                    
                    if inbounds(A.shape, x2, y2):
                        antinodes[x2, y2] = True

                else:

                    antinodes[*a1] = True
                    antinodes[*a2] = True

                    x1, y1 = a1 - diff
                    while inbounds(A.shape, x1, y1):
                        antinodes[x1, y1] = True
                        x1, y1 = x1 - diff[0], y1 - diff[1]
                    
                    x1, y1 = a2 + diff
                    while inbounds(A.shape, x1, y1):
                        antinodes[x1, y1] = True
                        x1, y1 = x1 + diff[0], y1 + diff[1]

    return antinodes

def visualize(A, antinodes):

    visual = np.copy(A)
    visual[*np.where(antinodes)] = "#"
    return visual

if __name__ == "__main__":

    _in = aocd.get_data(year = 2024, day = 8)

    # Parse Input
    A = np.array([[char for char in line.strip()] for line in _in.split("\n")])

    # Part 1
    print(np.sum(find_antinodes(A)))

    # Part 2
    print(np.sum(find_antinodes(A, False)))