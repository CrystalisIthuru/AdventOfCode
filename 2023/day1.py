import re
import os

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE_1 = os.path.join(INPUT_DIRECTORY, "1.dat")

def text2int(s):
    
    map = {
        "one" : 1,
        "two" : 2,
        "three" : 3,
        "four" : 4,
        "five" : 5,
        "six" : 6,
        "seven" : 7,
        "eight" : 8,
        "nine" : 9,
    }

    if s in map:
        return map[s]
    else:
        return int(s)

calibrations = []
with open(INPUT_FILE_1, "r") as f:
    for line in f:
 
        #matches = [m.group(1) for m in re.finditer(r"(?=(\d))", line)]
        matches = [m.group(1) for m in re.finditer(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))", line)]

        calibration = text2int(matches[0]) * 10 + text2int(matches[-1])
        calibrations += [calibration]

print(sum(calibrations))