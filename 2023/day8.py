from functools import reduce
import math
import multiprocessing as mp
import os
import re

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "8.dat")

class GraphNode:

    def __init__(self, label, left, right):

        self.label = label
        self.left = left
        self.right = right

    def __repr__(self):

        return f"{self.label} = ({self.left}, {self.right})"

def parse_input(input_file):

    with open(input_file, "r") as f:

        instructions = f.readline().strip()
        f.readline() # Skip a line

        nodes = {}

        for line in f:
            match = re.match(r"(.{3}) = \((.{3})\, (.{3})\)", line)
            
            label = match.group(1)
            left = match.group(2)
            right = match.group(3)

            nodes[label] = GraphNode(label, left, right)

    return instructions, nodes

def evaluate_instructions(instructions, nodes, starting_node, final_node):

    current_node = starting_node
    total_steps = 0
    while current_node != final_node:
        current_node, steps = find_next_node(instructions, current_node, nodes)
        total_steps += steps

    return total_steps

def evaluate_instructions_ghost(instructions, nodes, starting_char, final_char):

    starting_nodes = find_starting_nodes(nodes, "A")
    node_steps = []
    for node in starting_nodes:

        steps = 0
        current_node = node
        while current_node[-1] != final_char:
            current_node, _ = find_next_node(instructions, current_node, nodes)
            steps += len(instructions)

        node_steps += [steps]

    return reduce(lambda acc, x: abs(acc * x) // math.gcd(acc, x), node_steps, 1) # Calculates least common multiple

NEXT_NODE_CACHE = {}
def find_next_node(instructions, current_node, nodes):

    if current_node in NEXT_NODE_CACHE:
        return NEXT_NODE_CACHE[current_node], len(instructions)

    starting_node = current_node
    steps = 0
    for instruction in instructions:
        if instruction == "L":
            current_node = nodes[current_node].left
        else:
            current_node = nodes[current_node].right
        steps += 1

    NEXT_NODE_CACHE[starting_node] = current_node
    return current_node, steps

def find_starting_nodes(nodes, starting_char):

    return list(filter(lambda x: x[-1] == starting_char, nodes.keys()))

if __name__ == "__main__":

    instructions, nodes = parse_input(INPUT_FILE)

    print(evaluate_instructions(instructions, nodes, "AAA", "ZZZ"))
    print(evaluate_instructions_ghost(instructions, nodes, "A", "Z"))