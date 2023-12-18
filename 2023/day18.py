from functools import reduce
import numpy as np
import os
import re
import sys

sys.setrecursionlimit(1000000)

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "18.dat")


def build_vertices(instructions):

    vertices = [(0, 0)]
    for direction, length, color in instructions:
        prev_vertex = vertices[-1]
        vertex = move_vertex(prev_vertex, direction, length)
        vertices += [vertex]

    return vertices[:-1]

def move_vertex (vertex, direction, length):

    i, j = vertex
    if direction == "R":
        return (i, j + length)
    elif direction == "L":
        return (i, j - length)
    elif direction == "U":
        return (i - length, j)
    elif direction == "D":
        return (i + length, j)
    else:
        raise Exception(f"Unknown direction '{directions}'")

def parse_input(input_file):

    instructions = []

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                match = re.match(r"(R|D|L|U) (\d+) \(#([A-Za-z0-9]{6})\)", line)

                direction = match.group(1)
                length = int(match.group(2))
                color = match.group(3)

                instructions += [(direction, length, color)]

    return instructions

def shoelace_area(vertices):

    area = 0
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        if i == len(vertices) - 1:
            x2, y2 = vertices[0]
        else:
            x2, y2 = vertices[i + 1]
        
        area += x1 * y2 - x2 * y1

    return abs(area / 2)

def internal_points_from_picks(A, b):

    return A - (b / 2) + 1

def count_boundary(vertices):

    boundary_count = 0
    for i in range(len(vertices)):

        x1, y1 = vertices[i]
        if i == len(vertices) - 1:
            x2, y2 = vertices[0]
        else:
            x2, y2 = vertices[i + 1]

        if x1 != x2:
            boundary_count += abs(x2 - x1)
        else:
            boundary_count += abs(y2 - y1)
    
    return boundary_count

def translate_vertices(vertices):

    min_x = min(map(lambda x: x[0], vertices))
    min_y = min(map(lambda x: x[1], vertices))

    return list(map(lambda x: (x[0] + min_x, x[1] + min_y), vertices))

def count_lava(vertices):

    area = shoelace_area(vertices)
    boundary_count = count_boundary(vertices)
    internal_count = internal_points_from_picks(area, boundary_count)

    return int(boundary_count + internal_count)

def convert_instructions(instructions):

    directions =["R", "D", "L", "U"]

    new_instructions = []
    for _, _, color in instructions:

        distance = int(color[:-1], 16)
        direction = directions[int(color[-1])]

        new_instructions += [(direction, distance, None)]

    return new_instructions 

if __name__ == "__main__":

    instructions = parse_input(INPUT_FILE)
    vertices = translate_vertices(build_vertices(instructions))
    print(count_lava(vertices))

    vertices = translate_vertices(build_vertices(convert_instructions(instructions)))
    print(count_lava(vertices))
