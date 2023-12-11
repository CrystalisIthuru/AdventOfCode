import functools
import os
import re

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "6.dat")

def parse_input_pt1(input_file):

    with open(input_file, "r") as f:
        times = [int(n) for n in re.findall(r"\d+", f.readline())]
        distances = [int(n) for n in re.findall(r"\d+", f.readline())]

    return times, distances

def parse_input_pt2(input_file):

    times, distance = parse_input_pt1(input_file)

    time = int(functools.reduce(lambda acc, x: acc + str(x), times, ""))
    distance = int(functools.reduce(lambda acc, x: acc + str(x), distance, ""))

    return time, distance

def calculate_distance(time, velocity):

    return velocity * time

def record_combo(time, distance):

    for i in range(time + 1):
        d = calculate_distance(time - i, i)
        if d > distance:
            return (time - i) - i + 1

if __name__ == "__main__":

    times, distances = parse_input_pt1(INPUT_FILE)

    beat_record_combos = [record_combo(time, distance) for time, distance in zip(times, distances)]
    print(functools.reduce(lambda acc, x: acc * x, beat_record_combos, 1))

    time, distance = parse_input_pt2(INPUT_FILE)
    print(record_combo(time, distance))
