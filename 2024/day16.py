import aocd
import enum
import heapq
import numpy as np

EXAMPLE = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""".strip()

EXAMPLE2 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""".strip()

EXAMPLE3 = """
###########################
#######################..E#
######################..#.#
#####################..##.#
####################..###.#
###################..##...#
##################..###.###
#################..####...#
################..#######.#
###############..##.......#
##############..###.#######
#############..####.......#
############..###########.#
###########..##...........#
##########..###.###########
#########..####...........#
########..###############.#
#######..##...............#
######..###.###############
#####..####...............#
####..###################.#
###..##...................#
##..###.###################
#..####...................#
#.#######################.#
#S........................#
###########################
""".strip()

class Direction(enum.Enum):

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __lt__(self, o):
        return self.value < o.value

MOVEMENTS = {
    Direction.UP    : [-1,  0],
    Direction.DOWN  : [ 1,  0],
    Direction.LEFT  : [ 0, -1],
    Direction.RIGHT : [ 0,  1],
}

def solve_maze(maze):

    start = tuple([int(n) for n in np.argwhere(maze == "S")[0,:]])
    end = tuple([int(n) for n in np.argwhere(maze == "E")[0,:]])

    def dijkstras():

        costs = np.full((*maze.shape, 4), -1, dtype = int)
        costs[(*start, Direction.RIGHT.value)] = 0
        prev = { (*start, Direction.RIGHT.value) : {} }
        
        # Queue will be a priority queue with the cost
        # as the first element, then a tuple containing
        # the position and direction as the second
        queue = [(0, (start, Direction.RIGHT))]

        while queue:

            score, (loc, current_direction) = heapq.heappop(queue)

            directions = [
                (Direction((current_direction.value + 1) % 4), 1),
                (Direction((current_direction.value - 1) % 4), 1),
                (current_direction, 0)
            ]

            forward = loc[0] + MOVEMENTS[current_direction][0], loc[1] + MOVEMENTS[current_direction][1]
            states = [
                (loc, Direction((current_direction.value + 1) % 4), 1000),
                (loc, Direction((current_direction.value - 1) % 4), 1000),
                (forward, current_direction, 1)
            ]

            for pos, direction, dscore in states:

                if maze[*pos] == "#":
                    continue

                cost = score + dscore
                if costs[*pos, direction.value] == -1 or cost < costs[*pos, direction.value]:

                    costs[*pos, direction.value] = cost
                    prev[*pos, direction.value] = {(*loc, current_direction.value)}
                    
                    # Update Priority Queue. Replace element and rebuild heap
                    # if it already exists in the queue, or just add it. This
                    # satisfies the decrease priority step of Dijkstras
                    for i, (_cost, el) in enumerate(queue):
                        if el == (cost, direction):
                            queue[i] = (cost, (pos, direction))
                            heapq.heapify(queue)
                            break
                    else:
                        heapq.heappush(queue, (cost, (pos, direction)))
                elif costs[*pos, direction.value] == -1 or cost <= costs[*pos, direction.value]:
                    prev[*pos, direction.value].add((*loc, current_direction.value))

        queue = [(*end, 0)]
        tiles = set()
        while queue:
            current = queue.pop(-1)
            tiles.add(current[:-1])
            for next in prev[current]:
                if next not in tiles:
                    queue += [next]
         
        return costs, len(tiles)
 
    costs, tile_count = dijkstras()
    return np.min(costs[*end]), tile_count

if __name__ == "__main__":

    _in = aocd.get_data(year = 2024, day = 16)

    # Parse Input
    maze = np.array([[char for char in line.strip()] for line in _in.split("\n")])

    # Part 1
    start = np.argwhere(maze == "S")[0,:]
    print(*solve_maze(np.copy(maze)))