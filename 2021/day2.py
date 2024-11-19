import aocd
import re
import numpy as np

def parseInput(input):

    commands = []
    for line in input.split("\n"):
        direction, distance = re.split(r"\s+", line.strip())
        commands += [(direction, int(distance))]
    
    return commands

def run_commands(commands, start = (0, 0)):
    
    def move(direction, distance, position):
        x, y = position
        if direction == "forward":
            return x + distance, y
        elif direction == "down":
            return x, y + distance
        elif direction == "up":
            return x, y - distance
        else:
            raise Exception(f"Unknown Direction: '{direction}'")

    position = start
    for direction, distance in commands:
        position = move(direction, distance, position)
    return position

def run_commands_pt2(commands, start = (0, 0, 0)):
    
    def move(direction, distance, position):
        x, y, aim = position
        if direction == "forward":
            return x + distance, y + distance * aim, aim
        elif direction == "down":
            return x, y, aim + distance
        elif direction == "up":
            return x, y, aim - distance
        else:
            raise Exception(f"Unknown Direction: '{direction}'")

    position = start
    for direction, distance in commands:
        position = move(direction, distance, position)
    return position[:-1]

if __name__ == "__main__":

    commands = parseInput(aocd.get_data(day = 2, year = 2021))

    # Part 1
    print(np.prod(run_commands(commands)))

    # Part 2
    print(np.prod(run_commands_pt2(commands)))