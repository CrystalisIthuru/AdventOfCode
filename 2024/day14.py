from PIL import Image

import aocd
import functools
import numpy as np
import os
import re

EXAMPLE = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip()

EXAMPLE2 = """
p=2,4 v=2,-3
""".strip()

class Robot:

    def __init__(self, pos, vel):

        self.pos = pos
        self.vel = vel
    
    def __repr__(self):

        return f"<Robot {self.pos} {self.vel}>"
    
def move_robots(robots, shape, time):

    result = []
    for robot in robots:
        new_position = robot.pos + robot.vel * time
        new_position[0] = new_position[0] % shape[1]
        new_position[1] = new_position[1] % shape[0]
        result += [Robot(new_position, robot.vel)]

    return result

def count_robots(shape, robots):

    positions = {}
    for robot in robots:
        pos = tuple(robot.pos)
        if pos not in positions:
            positions[pos] = 1
        else:
            positions[pos] += 1

    counts = np.zeros(shape, dtype = int)
    for k, v in positions.items():
        counts[k[1], k[0]] = v
    
    return counts


def visualize(counts):

    visual = np.full(counts.shape, ".")
    for (i, j), el in np.ndenumerate(counts):
        if el > 0:
            visual[i, j] = str(el)
    
    return visual

def partition_quadrants(counts):

    half_x = counts.shape[0] // 2
    half_y = counts.shape[1] // 2

    top_left = counts[:half_x, :half_y]
    top_right = counts[:half_x, half_y+1:]
    bot_left = counts[half_x+1:, :half_y]
    bot_right = counts[half_x+1:, half_y+1:]
    
    #print(top_left)
    #print(top_right)
    #print(bot_left)
    #print(bot_right)

    quadrants = [top_left, top_right, bot_left, bot_right]
    return functools.reduce(lambda acc, x: acc * np.sum(x), quadrants, 1)

if __name__ == "__main__":

    _in = EXAMPLE
    _in = aocd.get_data(year = 2024, day = 14)

    # Parse Input
    robots = []
    for line in _in.split("\n"):
        numbers = [int(n) for n in re.findall(r"-?\d+", line)]
        robots += [Robot(np.array(numbers[:2]), np.array(numbers[2:]))]

    # Part 1
    shape = (7, 11)
    shape = (103, 101)
    print(partition_quadrants(count_robots(shape, move_robots(robots, shape, 100))))

    # Part 2
    print("Generating Robots Gif, checkout frame 6752")
    robots = []
    for line in _in.split("\n"):
        numbers = [int(n) for n in re.findall(r"-?\d+", line)]
        robots += [Robot(np.array(numbers[:2]), np.array(numbers[2:]))]

    frames = [] 
    for _ in range(10000):

        robots = move_robots(robots, shape, 1)
        counts =  count_robots(shape, robots)
        frame = np.where(counts > 0, 255, 0).astype(np.uint8)
        frames += [Image.fromarray(frame)]

    frames[0].save("robots.gif", append_images = frames[1:], save_all = True, duration = 100, loop = 0)