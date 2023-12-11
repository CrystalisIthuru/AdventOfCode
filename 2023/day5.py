import collections
import functools
import os
import re

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "5.dat")

class ClosedInterval:

    def __init__(self, lower, upper):

        self.lower = lower
        self.upper = upper

    def __add__(self, other):

        if isinstance(other, int):
            return ClosedInterval(self.lower + other, self.upper + other)
        else:
            return ClosedInterval(self.lower + other.lower, self.upper + other.upper)

    def __contains__(self, value):

        return self.lower <= value <= self.upper
    
    def __eq__(self, other):

        return self.lower == other.lower and self.upper == other.upper
    
    def __repr__(self):
        return f"<ClosedInterval [{self.lower}, {self.upper}]>"

    def difference(self, other):

        if self == other:
            return None
        elif other.lower <= self.upper <= other.upper:
            return [ClosedInterval(self.lower, self.upper - (self.upper - other.lower))]
        elif other.lower <= self.lower <= other.upper:
            return [ClosedInterval(self.lower + (other.upper - self.lower), self.upper)]
        elif self.lower <= other.lower and self.upper >= other.upper:
            return [
                ClosedInterval(self.lower, other.lower),
                ClosedInterval(other.upper, self.upper)
            ]
        else:
            raise TypeError(f"{self} {other}")
    
    def intersect(self, other):

        if self.upper <= other.lower or other.upper <= self.lower:
            return None
        
        return ClosedInterval(max(self.lower, other.lower), min(self.upper, other.upper))
         
class AlmanacMap:

    def __init__(self, destination, source, length):

        self._source = source
        self._destination = destination
        self._length = length

    def __contains__(self, value):
        return value >= self._source and value < self._source + self._length
    
    def __getitem__(self, key):

        if key not in self:
            raise KeyError(f"'{key}' not within range [{self._source},{self._source + self._destination})")
        
        return self._destination + (key - self._source)
    
    def __repr__(self):

        return f"<AlmanacMap {self._source} {self._destination} {self._length}>"
    
    def asIntervals(self):

        source_interval = ClosedInterval(self._source, self._source + self._length)
        destination_interval   = ClosedInterval(self._destination, self._destination + self._length)

        return source_interval, destination_interval


def parse_input(input_file):

    with open(input_file, "r") as f:
        data = f.read()

    scanner = re.Scanner([
        (r"seeds: (?:\d+\s*)+", lambda scanner, match: ("SEEDS_DATA", match.strip())),
        (r".*\s*map:", lambda scanner, match: ("MAP_DECLARATION", match.strip())),
        (r"(?:\d+[ \t]*)+", lambda scanner, match: ("MAP_RANGE", match.strip())),
        (r"\s*", None)
    ])

    tokens, _ = scanner.scan(data)

    seed_token_type, seed_data = tokens.pop(0)
    seeds = [int(n) for n in re.findall("\d+", seed_data)]

    almanac_maps = collections.OrderedDict()
    current_map = ""
    while len(tokens) > 0:

        token_type, token_data = tokens.pop(0)
        if token_type == "MAP_DECLARATION":
            match = re.search(r"(.*)\s+map:", token_data)
            map_name = match.group(1)
            current_map = map_name
            if current_map not in almanac_maps:
                almanac_maps[current_map] = []
        elif token_type == "MAP_RANGE":
            source, destination, length = [int(n) for n in re.findall(r"\d+", token_data)]
            almanac_maps[current_map] += [AlmanacMap(source, destination, length)]
        else:
            raise TypeError(f"Unknown token type '{token_type}'")

    return seeds, almanac_maps

def evaluate_seed(seed, almanac_maps):

    path = [seed]
    for map_name, maps in almanac_maps.items():
        for map in maps:
            if path[-1] in map:
                path += [map[path[-1]]]
                break
        else:
            path += [path[-1]]
    return path[-1]

def map_interval(interval, almanac_maps):

    interval_queue = [interval]
    for almanac_map in list(almanac_maps.keys()):
        map_intervals = [m.asIntervals() for m in almanac_maps[almanac_map]]
        #print(almanac_map)
        #print(interval_queue)
        #print(map_intervals)
        intervals = []
        while interval_queue:
            interval = interval_queue.pop(0)

            for source, destination in map_intervals:
                interval_transform = lambda interval: interval + (destination.lower - source.lower)

                intersect = interval.intersect(source)
                #print("Test: ", intersect, interval, source)

                if intersect:
                    intervals += [interval_transform(intersect)]
                    if intersect != interval:
                        interval_queue += interval.difference(intersect)
                    break
            
            else:
                intervals += [interval]

        interval_queue = intervals

    return interval_queue

if __name__ == "__main__":

    seeds, almanac_maps = parse_input(INPUT_FILE)

    print(min([evaluate_seed(seed, almanac_maps) for seed in seeds]))

    seed_intervals = [ClosedInterval(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]

    location_intervals = functools.reduce(lambda acc, interval: acc + map_interval(interval, almanac_maps), seed_intervals, [])
    print(sorted(location_intervals, key = lambda x: x.lower)[0].lower)

        