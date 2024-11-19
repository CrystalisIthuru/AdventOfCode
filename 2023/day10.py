import aocd
import numpy as np
import re
import sys

sys.setrecursionlimit(1000000)

class GraphNode:

    def __init__(self, position, pipe, children = [], is_start = False):

        self.position = position
        self.children = [child for child in children if child is not None]
        self.is_start = is_start
        self.pipe = pipe

    def __repr__(self):

        return self.pipe

def parse_input(input):

    lines = [line.strip() for line in input.split("\n")]
    pipes = np.array([re.split(r"", line.strip())[1:-1] for line in lines if len(line) != 0])
    return pipes

def traverse_pipes(start, graph):

    traverse = np.zeros_like(graph, dtype = int)
    
    traverse_queue = [start]
    traverse[start.position] = -1
    traverse_count = 0

    while len(traverse_queue) > 0:
        new_queue = []
        for node in traverse_queue:
            if traverse_count != 0: traverse[node.position] = traverse_count
            new_queue += [graph[i, j] for i, j in node.children if traverse[i, j] == 0]
        traverse_count += 1
        traverse_queue = new_queue

    return traverse

def find_cycle(graph, traverse):

    cycle_end = np.unravel_index(np.argmax(traverse), traverse.shape)
    cycle_end_node = graph[cycle_end]


    path_indices = [cycle_end_node.position]
    for child in cycle_end_node.children:
        path = depth_first_search(graph, traverse, graph[child], np.amax(traverse) - 1)
        path_indices += [node.position for node in path]

    cycle = np.zeros_like(traverse, dtype = int)
    for index in path_indices:
        cycle[index] = 1

    return cycle

def depth_first_search(graph, traverse, node, expected_value):

    node_value = traverse[node.position]
    if node_value == -1:
        return [node]
    elif node_value == expected_value:
        for child in node.children:
            child_path = depth_first_search(graph, traverse, graph[child], expected_value - 1)
            if child_path is not None:
                return [node] + child_path
        else:
            return None
    else:
        return None 

def find_internal_points(cycle):

    count = np.zeros_like(cycle)
    for i, j in np.ndindex(cycle.shape):

        if cycle[i, j] == 0:
            left = np.sum(cycle[i,:j])
            right = np.sum(cycle[i,j:])
            if left % 2 != 0 and right % 2 != 0:
                count[i, j] = 1

    return count

def create_graph(pipes):

    graph = np.full(pipes.shape, None)

    for (i, j), pipe in np.ndenumerate(pipes):

        top_child = (i - 1, j) if i > 0 else None
        bottom_child = (i + 1, j) if i < pipes.shape[0] else None
        left_child = (i, j - 1) if j > 0 else None
        right_child = (i, j + 1) if j < pipes.shape[1] else None

        if pipe == "|":
            graph[i, j] = GraphNode((i, j), pipe, children = [top_child, bottom_child])
        elif pipe == "-":
            graph[i, j] = GraphNode((i, j), pipe, children = [left_child, right_child])
        elif pipe == "L":
            graph[i, j] = GraphNode((i, j), pipe, children = [top_child, right_child])
        elif pipe == "J":
            graph[i, j] = GraphNode((i, j), pipe, children = [top_child, left_child])
        elif pipe == "7":
            graph[i, j] = GraphNode((i, j), pipe, children = [left_child, bottom_child])
        elif pipe == "F":
            graph[i, j] = GraphNode((i, j), pipe, children = [bottom_child, right_child])
        elif pipe == "S":
            graph[i, j] = GraphNode((i, j), pipe, is_start = True)
        elif pipe == ".":
            graph[i, j] = GraphNode((i, j), pipe)
        else:
            raise TypeError(f"Unknown pipe '{pipe}'")

    return graph

def find_starting_node(pipes, graph):

    starting_node = graph[np.where(pipes == "S")][0]
    i, j = starting_node.position

    if i > 0 and pipes[i - 1, j] in ["|", "7", "F"]:
        starting_node.children += [(i - 1, j)]
    if i < pipes.shape[0] and pipes[i + 1, j] in ["|", "L", "J"]:
        starting_node.children += [(i + 1, j)]
    if j > 0  and pipes[i, j - 1] in ["-", "L", "F"]:
        starting_node.children += [(i, j - 1)]
    if j < pipes.shape[0] and pipes[i, j + 1] in ["-", "J", "7"]:
        starting_node.children += [(i, j + 1)]

    return starting_node

def expand_pipes(pipes):

    left_facing_pipes = ["S", "-", "L", "F"]
    right_facing_pipes = ["S", "-", "7", "J"]
    top_facing_pipes = ["S", "|", "7", "F"]
    bot_facing_pipes = ["S", "|", "L", "J"]

    expanded = np.zeros((pipes.shape[0] * 2, pipes.shape[1] * 2), dtype = pipes.dtype)
    indices = np.indices(pipes.shape) * 2
    expanded[indices[0], indices[1]] = pipes

    for (i, j), value in np.ndenumerate(expanded):

        if len(value) == 0:
            
            top = expanded[i - 1, j] if i > 0 else None
            bot = expanded[i + 1, j] if i < expanded.shape[0] - 1 else None
            left = expanded[i, j - 1] if j > 0 else None
            right = expanded[i, j + 1] if j < expanded.shape[1] - 1 else None

            if left in left_facing_pipes and right in right_facing_pipes:
                expanded[i, j] = "-"
            elif top in top_facing_pipes and bot in bot_facing_pipes:
                expanded[i, j] = "|"
            else:
                expanded[i, j] = "."

    return expanded, indices

def flood_fill(cycle):

    r, c = cycle.shape
    filled = np.copy(cycle)
    indices = np.indices(filled.shape)

    fill_positions = []
    for i in range(r):
        if cycle[i, 0] == 0:
            fill_positions += [(i, 0)]
        elif cycle[i, c - 1] == 0:
            fill_positions += [(i, c - 1)]

    for i in range(c):
        if cycle[0, i] == 0:
            fill_positions += [(0, i)]
        elif cycle[r - 1, i] == 0:
            fill_positions += [(r - 1, i)]

    for position in fill_positions:
        filled = flood_fill_recur(filled, position)
    
    return filled    

def flood_fill_recur(filled, position):

    r, c = filled.shape

    x, y = position
    filled[position] = 1
    for i in range(-1, 2):
        for j in range(-1, 2):

            dx, dy = x + i, y + j
            
            if dx < 0 or dy < 0 or dx > r - 1 or dy > c - 1: continue

            if filled[x + i, y + j] == 0:
                flood_fill_recur(filled, (x + i, y + j))

    return filled

if __name__ == "__main__":

    pipes = parse_input(aocd.get_data(day = 10, year = 2023))

    pipes, indices = expand_pipes(pipes)
    graph = create_graph(pipes)
    start = find_starting_node(pipes, graph)
    traverse = traverse_pipes(start, graph)

    cycle = find_cycle(graph, traverse)
    filled = flood_fill(cycle)
    filled = filled[indices[0], indices[1]] # Reduce back to original shape

    print(np.max(traverse) // 2)
    print(np.sum(np.logical_not(filled.astype(bool)))) 
