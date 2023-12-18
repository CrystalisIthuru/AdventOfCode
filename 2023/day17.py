import os
import numpy as np
import heapq

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "17-test.dat")
    
def count_distance(path, direction):

    if direction not in ["vertical", "horizontal"]:
        raise Exception(f"Unknown direction {direction}")
    
    path_index = 0 if direction == "horizontal" else 1
    count = 0
    for i in range(1, len(path)):
        if path[i - 1].location[path_index] == path[i].location[path_index]:
            count += 1
        else:
            return count
    return count

def path_too_long(path, location):

    if len(path) <= 0: return False
 
    if path[0].location[0] == location[0]:
        direction = "horizontal"
    elif path[0].location[1] == location[1]:
        direction = "vertical"
    else:
        raise Exception()

    return count_distance(path, direction) > 2

class GraphNode:

    def __init__(self, location):

        self.location = location
        self.distance = 999999999999999
        self.prev = None
        self.visited = False

    def __repr__(self):

        if self.prev:

            x0, y0 = self.location
            x1, y1 = self.prev.location

            if x1 < x0:
                return "v"
            elif x0 < x1:
                return "^"
            elif y1 < y0:
                return ">"
            elif y0 < y1:
                return "<"
            else:
                raise Exception()
        else:
            return "-"

    def get_path(self):

        path = []
        node = self
        while node:
            path += [node]
            node = node.prev

        return path

def parse_input(input_file):

    graph = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                graph += [[int(char) for char in line]]
    
    return np.array(graph)

def get_neighbors(node, shape):

    r, c = shape
    i, j = node

    neighbors = []
    if i > 0: neighbors += [(i - 1, j)]
    if j > 0: neighbors += [(i, j - 1)]
    if i < r - 1: neighbors += [(i + 1, j)]
    if j < c - 1: neighbors += [(i, j + 1)]

    return neighbors

def dijkstra(graph):

    queue = []

    nodes = np.full(graph.shape, None)
    for index in np.ndindex(nodes.shape):
        nodes[index] = GraphNode(index)
        queue += [nodes[index]]

    for node in get_neighbors((0, 0), nodes.shape):
        nodes[node].distance = 0

    queue = sorted(queue, key = lambda x: x.distance)
    while queue:
        u = queue.pop(0)
        u.visited = True

        neighbors = get_neighbors(u.location, nodes.shape)
        neighbors = filter(lambda neighbor: not nodes[neighbor].visited, neighbors)
        neighbors = filter(lambda neighbor: not path_too_long(u.get_path(), neighbor), neighbors)
        for neighbor in neighbors:
            v = nodes[neighbor]
            alt = u.distance + graph[neighbor]
            if alt < v.distance:
                v.distance = alt
                v.prev = u

        queue = sorted(queue, key = lambda x: x.distance)

    print(nodes)
    final_path = nodes[-1, -1].get_path()
    test = np.zeros_like(graph)
    for index in final_path:
        test[index.location] = 1
    print(test)

    print(np.sum(graph[np.where(test == 1)]))

if __name__ == "__main__":

    graph = parse_input(INPUT_FILE)
    dijkstra(graph)