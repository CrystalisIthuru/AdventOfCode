import os
import re
from collections import OrderedDict

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "15.dat")

def HASH(str):

    current_value = 0
    for char in str:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256

    return current_value

def parse_input(input_file):

    instructions = []
    with open(input_file, "r") as f:
        for line in f:
            instructions += line.split(",")

    return instructions

def arange_lenses(instructions):

    boxes = [None] * 256

    for instruction in instructions:

        match = re.match(r"([^=-]+)(=|-)(\d*)", instruction)
        label = match.group(1)
        operation = match.group(2)

        label_index = HASH(label)

        if operation == "=":

            focal_length = int(match.group(3))
            if boxes[label_index] is None: boxes[label_index] = []

            box = boxes[label_index]
            for i, (l, fl) in enumerate(box):
                if label == l:
                    box[i] = (label, focal_length)
                    break
            else:
                box += [(label, focal_length)]

        elif operation == "-":
            if boxes[label_index] is not None:
                box = boxes[label_index]
                for i, (l, fl) in enumerate(box):
                    if label == l:
                        del box[i]
                        break
        else:
            raise Exception(f"Unknown operation {operation}")


    focusing_power = 0
    for i, box in filter(lambda box: box[1] is not None and len(box[1]) != 0, enumerate(boxes)):
        for j, (label, focal_length) in enumerate(box):
            focusing_power += (i + 1) * (j + 1) * focal_length

    return focusing_power

if __name__ == "__main__":

    instructions = parse_input(INPUT_FILE)
    print(sum(map(HASH, instructions)))
    print(arange_lenses(instructions))