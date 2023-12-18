import os
import numpy as np
import heapq

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "17-test.dat")

class GraphNode:

    def __init__(self, location):

        self.location = location
        self.value = None
        self.prev = None
        self.visited = False

    def __lt__(self, other):

        return self.location < other.location

    def __repr__(self):

        if self.prev:

            x0, y0 = self.location
            x1, y1 = self.prev.location

            if x0 < x1:
                return "v"
            elif x1 < x0:
                return "^"
            elif y0 < y1:
                return ">"
            else:
                return "<"
        else:
            return "-"

    def get_path(self):

        path = []
        node = self
        while node:
            path += [node]
            node = node.prev

        return path

    def too_long(self, location):

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
        
        if self.location[0] == location[0]:
            direction = "horizontal"
        elif self.location[1] == location[1]:
            direction = "vertical"
        else:
            raise Exception()

        count = count_distance(self.get_path(), direction)

        print(count, self.location, location, direction)

        return count > 2

def parse_input(input_file):

    graph = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                graph += [[int(char) for char in line]]
    
    return np.array(graph)

def dijkstra(graph):

    nodes = np.full(graph.shape, None)
    for index, value in np.ndenumerate(graph):
        nodes[index] = GraphNode(index)

    queue = [(graph[node], nodes[node]) for node in get_neighbors((0, 0), graph.shape)]
    heapq.heapify(queue)

    while queue:
        value, node = heapq.heappop(queue)

        if node.visited: continue

        # Mark Node
        node.visited = True
        node.value = value

        # Update neighbors
        neighbors = [nodes[neighbor] for neighbor in get_neighbors(node.location, graph.shape) if not node.too_long(neighbor)]
        print("Dij: ", node.location, value, [n.location for n in neighbors])
        for neighbor in neighbors:
            distance = value + graph[neighbor.location]
            if neighbor.value is None or distance < neighbor.value:
                neighbor.value = distance
                neighbor.prev = node
                heapq.heappush(queue, (distance, neighbor))


    print(graph.shape)
    print(nodes)

    test = np.zeros_like(graph)
    for node in nodes[-1, -1].get_path():
        test[node.location] = 1
    print(test)

def get_neighbors(node, shape):

    r, c = shape
    i, j = node

    neighbors = []
    if i > 0: neighbors += [(i - 1, j)]
    if j > 0: neighbors += [(i, j - 1)]
    if i < r - 1: neighbors += [(i + 1, j)]
    if j < c - 1: neighbors += [(i, j + 1)]

    return neighbors

if __name__ == "__main__":

    graph = parse_input(INPUT_FILE)
    dijkstra(graph)