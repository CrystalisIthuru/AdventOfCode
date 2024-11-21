import aocd
import numpy as np

EXAMPLE = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""

def find_lowest_points(map):

    points = []
    for i, j in np.ndindex(map.shape):

        if (i - 1 >= 0 and map[i, j] >= map[i - 1, j]) or \
           (j - 1 >= 0 and map[i, j] >= map[i, j - 1]) or \
           (i + 1 < map.shape[0] and map[i, j] >= map[i + 1, j]) or \
           (j + 1 < map.shape[1] and map[i, j] >= map[i, j + 1]):
            pass
        else:
            points += [(i, j)]

    points = np.array(points)
    return points[:,0], points[:,1]

def find_basins(map):

    lowest_x, lowest_y = find_lowest_points(map)

    basins = []
    for lowest in zip(lowest_x, lowest_y):

        basin_points = set()
        search_points = [lowest]

        while search_points:
            x, y = search_points.pop(0)
            basin_points.add((x, y))

            if x - 1 >= 0 and (x - 1, y) not in basin_points and map[x - 1, y] != 9:
                search_points += [(x - 1, y)]

            if x + 1 < map.shape[0] and (x + 1, y) not in basin_points and map[x + 1, y] != 9:
                search_points += [(x + 1, y)]

            if y - 1 >= 0 and (x, y - 1) not in basin_points and map[x, y - 1] != 9:
                search_points += [(x, y - 1)]
            
            if y + 1 < map.shape[1] and (x, y + 1) not in basin_points and map[x, y + 1] != 9:
                search_points += [(x, y + 1)]
        
        basins += [np.array(list(basin_points))]

    return basins

if __name__ == "__main__":

    input = EXAMPLE
    input = aocd.get_data(day = 9, year = 2021)

    # Part Input
    height_map = np.array([[int(char) for char in line.strip()] for line in input.split("\n") if len(line.strip()) > 0])

    # Part 1
    print(np.sum(height_map[*find_lowest_points(height_map)] + 1))

    # Part 2
    print(np.prod([x.shape[0] for x in sorted(find_basins(height_map), key = lambda x: x.shape[0], reverse = True)[:3]]))