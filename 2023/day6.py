import aocd
import functools
import re

def parse_input_pt1(input):

    lines = input.split("\n")
    times = [int(n) for n in re.findall(r"\d+", lines.pop(0))]
    distances = [int(n) for n in re.findall(r"\d+", lines.pop(0))]

    return times, distances

def parse_input_pt2(input):

    times, distance = parse_input_pt1(input)

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

    times, distances = parse_input_pt1(aocd.get_data(day = 6, year = 2023))

    beat_record_combos = [record_combo(time, distance) for time, distance in zip(times, distances)]
    print(functools.reduce(lambda acc, x: acc * x, beat_record_combos, 1))

    time, distance = parse_input_pt2(aocd.get_data(day = 6, year = 2023))
    print(record_combo(time, distance))
