import aocd
import numpy as np

def countIncreasingMeasurements(measurements):
    return np.sum(np.where(measurements[1:] - measurements[:-1] > 0, 1, 0))

def countIncreasingMeasurementsSlideingWindow(measurements, window):

    windowed_measurements = []
    for i in range(measurements.size - window + 1):
        windowed_measurements += [np.sum(measurements[i:i+window])]
    return countIncreasingMeasurements(np.array(windowed_measurements))

def parseInput(input):

    measurements = []
    for line in input.split("\n"):
        measurements += [int(line)]
    
    return np.array(measurements)

if __name__ == "__main__":

    measurements = parseInput(aocd.get_data(year = 2021, day = 1))

    # Part 1
    print(countIncreasingMeasurements(measurements))

    # Part 2
    print(countIncreasingMeasurementsSlideingWindow(measurements, 3))

    