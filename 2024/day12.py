import aocd
import numpy as np

EXAMPLE = """
AAAA
BBCD
BBCC
EEEC
""".strip()

EXAMPLE2 = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""".strip()

EXAMPLE3 = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".strip()

EXAMPLE4 = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
""".strip()

class Plot(set):

    def __init__(self, loc, neighbors):

        self.loc = loc
        self.neighbors = neighbors # neighbors within the region

    def __hash__(self):
        return hash(self.loc)

    def __eq__(self, o):
        return o == self.loc
    
    def __repr__(self):
        return f"<Plot {self.loc}>"

class Region:

    def __init__(self, plots, val):
        self.plots = plots
        self.val = val

    def __repr__(self):
        
        return f"<Region {len(self.plots)} {self.val}>"

def getNeighbors(A, loc, target = None):

    neighbors = [
        np.array([1, 0]),
        np.array([0, 1]),
        np.array([-1, 0]),
        np.array([0, -1])
    ]

    result = []
    for neighbor in neighbors:
        x, y = loc + neighbor
        if x < 0 or x >= A.shape[0] or y < 0 or y >= A.shape[1]:
            continue
        if target is None or A[x, y] == target:
            result += [(int(x), int(y))]

    return result

def find_regions(A):

    visited = set()
    regions = []
    for idx, el in np.ndenumerate(A):

        if idx in visited:
            continue

        plots = set()
        queue = [idx]
        while queue:
            next = queue.pop(0)
            if next in plots:
                continue

            neighbors = getNeighbors(A, next, el)

            queue += neighbors
            plots.add(Plot(next, set(neighbors)))
        
        regions += [Region(plots, el)]
        visited |= set([plot.loc for plot in plots])
    
    return regions

def check_corner(A, val, c, n1, n2):

    x, y = c
    x1, y1 = n1
    x2, y2 = n2

    # Line Configuration
    if x == x1 == x2 or y == y1 == y2:
        return 0
    
    # Corner Configuration
    else:

        x3 = x1 if x1 != x else x2
        y3 = y1 if y1 != y else y2

        # Outer Corner
        if A[x3, y3] != val:
            return 2
        
        # Inner Corner
        else:
            return 1

def count_sides(A, region):

    count = 0
    for plot in region.plots:
        x, y = plot.loc

        if len(plot.neighbors) == 0:
            count += 4
        elif len(plot.neighbors) == 1:
            count += 2
        elif len(plot.neighbors) == 2:

            n1 = list(plot.neighbors)[0]
            n2 = list(plot.neighbors)[1]

            count += check_corner(A, region.val, plot.loc, n1, n2)

        elif len(plot.neighbors) == 3:

            n1 = list(plot.neighbors)[0]
            n2 = list(plot.neighbors)[1]
            n3 = list(plot.neighbors)[2]

            count += check_corner(A, region.val, plot.loc, n1, n2)
            count += check_corner(A, region.val, plot.loc, n2, n3)
            count += check_corner(A, region.val, plot.loc, n1, n3)
            count -= 2 # Subtract the overcounting

        elif len(plot.neighbors) == 4:

            neighbors = list(plot.neighbors)
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if check_corner(A, region.val, plot.loc, neighbors[i], neighbors[j]) == 2:
                        count += 1

    return count

def find_fencing_cost(A):

    regions = find_regions(A)

    cost = 0
    bulk_cost = 0
    for region in regions:

        area = len(region.plots)
        perimeter = 0
        for plot in region.plots:
            perimeter += 4 - len(plot.neighbors)

        sides = count_sides(A, region)
#        print(region, sides, area, sides * area)
#        input()

        cost += area * perimeter 
        bulk_cost += area * sides
    
    return cost, bulk_cost

if __name__ == "__main__":

    _in = EXAMPLE3
    _in = aocd.get_data(year = 2024, day = 12)

    # Parse Input
    A = np.array([[char for char in line.strip()] for line in _in.split("\n")])

    # Part 1 and 2
    print(find_fencing_cost(A))