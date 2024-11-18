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
    with open(input, "r") as f:
        for line in f:
            measurements += [int(line)]
    
    return np.array(measurements)

if __name__ == "__main__":

    measurements = parseInput("inputs/1.dat")

    # Part 1
    print(countIncreasingMeasurements(measurements))

    # Part 2
    print(countIncreasingMeasurementsSlideingWindow(measurements, 3))

    