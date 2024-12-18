import aocd
import heapq
import numpy as np
import re

EXAMPLE = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""".strip()

EXAMPLE_SHAPE = (7, 7)
EXAMPLE_BYTECOUNT = 12

def bytes2obstacles(shape, bytes):

    obstacles = np.zeros(shape, dtype = bool)
    obstacles[bytes[:,1], bytes[:,0]] = True
    return obstacles

def dijkstras(obstacles, start, end):

    start = tuple(start)
    end = tuple(end)

    # Initialization
    costs = np.full(obstacles.shape, -1, dtype = int)
    costs[*start] = 0
    prev = { start : None }

    queue = [(0, start)]
    while queue:

        cost, node = heapq.heappop(queue)
        neighbors = get_neighbors(costs.shape, node)

        for neighbor in neighbors:

            # Can't move through obstacles
            if obstacles[*neighbor]:
                continue

            neighbor_cost = cost + 1
            if costs[*neighbor] == -1 or neighbor_cost < costs[*neighbor]:
                costs[*neighbor] = neighbor_cost
                prev[*neighbor] = node
                heapq.heappush(queue, (neighbor_cost, neighbor))

    path = []
    if end in prev:
        current = end
        while current:
            path += [current]
            current = prev[current]
    
    return costs, path

def get_neighbors(shape, loc):

    x, y = loc

    neighbors = []
    if x - 1 >= 0:
        neighbors += [(x - 1, y)]
    if y - 1 >= 0:
        neighbors += [(x, y - 1)]
    if x + 1 <= shape[0] - 1:
        neighbors += [(x + 1, y)]
    if y + 1 <= shape[1] - 1:
        neighbors += [(x, y + 1)]
    
    return neighbors

def visualize(obstacles, path):

    visual = np.full(obstacles.shape, ".")
    visual[np.where(obstacles)] = "#"

    for x, y in path:
        visual[x, y] = "O"

    return visual

if __name__ == "__main__":

    _in = EXAMPLE
    shape = EXAMPLE_SHAPE
    bytecount = EXAMPLE_BYTECOUNT

    _in = aocd.get_data(year = 2024, day = 18)
    shape = (71, 71)
    bytecount = 1024

    start = 0, 0
    end = shape[0] -1, shape[1] - 1

    # Parse Input
    bytes = []
    for line in _in.split("\n"):
        bytes += [[int(n) for n in re.findall(r"\d+", line)]]
    bytes = np.array(bytes)

    # Part 1
    obstacles = bytes2obstacles(shape, bytes[:bytecount,:])
    costs, path = dijkstras(obstacles, start, end)
    print(len(path) - 1)

    # Part 2
    # For part 2, we'll iterate through the remaining unplaced
    # bytes adding them one by one to the obstacle map. If one
    # of those bytes is in shortest path we will go looking 
    # for a new map until we cannot generate a new path.
    prev_path = path
    for i in range(bytecount, bytes.shape[0]):
        loc = bytes[i,1], bytes[i,0]
        obstacles[*loc] = True
        if loc in prev_path:
            _, prev_path = dijkstras(obstacles, start, end)
            if not prev_path:
                print(",".join(map(str, bytes[i,:])))
                break