import aocd
import numpy as np
import heapq

EXAMPLE = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".strip()

def dijkstras(A, start, end):

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

    costs = np.full(A.shape, -1, dtype = int)
    queue = [(0, start)]
    prev = { start : None }

    while queue:
        current_cost, current_loc = heapq.heappop(queue)

        neighbors = get_neighbors(A.shape, current_loc)
        for neighbor in neighbors:

            if A[*neighbor] == "#":
                continue

            ncost = current_cost + 1
            if costs[*neighbor] == -1 or ncost < costs[*neighbor]:
                costs[*neighbor] = ncost
                prev[*neighbor] = current_loc
                heapq.heappush(queue, (ncost, neighbor))

    path = []
    current = end
    while current != start:
        path = [current] + path
        current = prev[current]
    path = [start] + path

    return costs, path

def runner_times_with_cheating(track, start, end, cheat_time):

    _, path = dijkstras(track, start, end)

    # Maps the locations within the path with thier
    # index within the path. Quick reference to help
    # calculate how much time was saved when cheating
    path_map = { x : i for i, x in enumerate(path) }

    # Here we calculate the time saved by cheating. We compare the
    # manhattan distance of jumping to a location by cheating to
    # the distance we would have taken by just following the path
    # and saving that in the cheats map.
    cheats = {}
    for loc in path:
        for neighbor in get_neighbors_within_distance(track, loc, cheat_time):
            path_distance = path_map[*neighbor] - path_map[*loc]
            cheat_distance = manhattan(*neighbor, *loc)
            saved_time = path_distance - cheat_distance
            if saved_time > 0:
                cheats[loc, neighbor] = saved_time

    # Here we just count up the number of times X amount of time
    # was saved
    counts = {}
    for time in cheats.values():
        if time not in counts:
            counts[time] = 1
        else:
            counts[time] += 1

    return counts

def manhattan(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def get_neighbors_within_distance(track, loc, distance):

    # Here we calculate all valid neighbors that are within
    # ``distance`` manhattan distance from ``loc``

    neighbors = []
    for dx in range(-distance, distance+1):
        for dy in range(-distance, distance+1):
            x, y = loc[0] + dx, loc[1] + dy
            if x < 0 or y < 0 or x >= track.shape[0] or y >= track.shape[1] or (x, y) == loc or manhattan(x, y, *loc) > distance:
                continue
            if track[x, y] != "#":
                neighbors += [(x, y)]
    return neighbors

if __name__ == "__main__":

    _in = aocd.get_data(year = 2024, day = 20)

    # Parse Input
    track = np.array([[char for char in line.strip()] for line in _in.split("\n")])
    start = tuple([int(n) for n in np.argwhere(track == "S")[0,:]])
    end  = tuple([int(n) for n in np.argwhere(track == "E")[0,:]])

    # Part 1
    counts = runner_times_with_cheating(track, start, end, 2)
    print(sum([v for k, v in counts.items() if k >= 100]))

    # Part 2
    counts = runner_times_with_cheating(track, start, end, 20)
    print(sum([v for k, v in counts.items() if k >= 100]))