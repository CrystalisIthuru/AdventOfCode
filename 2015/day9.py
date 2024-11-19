import aocd
import numpy as np
import re
import copy

class GraphNode:

    def __init__(self, label):

        self.label = label
        self.edges = {}

    def add_edge(self, label, distance):

        self.edges[label] = distance

def create_distance_matrix(graph):
    
    distance = np.zeros((len(graph), len(graph)))

    label_indices = { label : i for i, label in enumerate(graph.keys()) }

    for label, node in graph.items():

        col_index = label_indices[label]
        for edge_label, edge_distance in node.edges.items():
            row_index = label_indices[edge_label]
            distance[row_index, col_index] = edge_distance

    return label_indices, distance

def create_graph(distances):

    nodes = {}
    for start, end, distance in distances:
        if start not in nodes: nodes[start] = GraphNode(start)
        if end not in nodes: nodes[end] = GraphNode(end)
        nodes[start].add_edge(end, distance)
        nodes[end].add_edge(start, distance)

    return nodes

def parse_input(input):

    distances = []
    for line in input.split("\n"):
        match = re.match(r"([a-zA-Z]+) to ([a-zA-Z]+) = (\d+)", line)

        distances += [(
            match.group(1),     # Start location
            match.group(2),     # End location
            int(match.group(3)) # Distance
        )]

    return distances

def get_permutations(elements, current_permutation = []):

    if elements:
        all_permutations = []
        for i in range(len(elements)):

            new_permutation = copy.deepcopy(current_permutation) + [elements[i]]

            new_elements = copy.deepcopy(elements)
            new_elements.remove(elements[i])

            all_permutations += get_permutations(new_elements, new_permutation)

        return all_permutations

    else:
        return [current_permutation]

def traveling_salesman(graph):

    permutations = get_permutations(list(graph.keys()))

    paths = []
    for path in permutations:
        distance = 0
        current_location = path[0]
        for next_location in path[1:]:
            distance += graph[current_location].edges[next_location]
            current_location = next_location
        
        paths += [(path, distance)]
    
    return paths

if __name__ == "__main__":

    distances = parse_input(aocd.get_data(day = 9, year = 2015))
    graph = create_graph(distances)
    distances = list(map(lambda x: x[1], traveling_salesman(graph)))
    print(min(distances))
    print(max(distances))