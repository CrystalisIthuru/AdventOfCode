import aocd
import numpy as np
import functools

def parseInput(input):

    matrix = []
    with open(input, "r") as f:
        for line in f:
            binary = []
            for char in line.strip():
                binary += [int(char)]
            matrix += [binary]
    return np.array(matrix)

def determineGammaAndEpislonRates(report):

    gamma_rate = np.where(np.sum(report, axis = 0) > (report.shape[0] / 2), 1, 0)
    epsilon_rate = np.where(np.logical_not(gamma_rate), 1, 0)

    return gamma_rate, epsilon_rate

def getPowerConsumption(report):

    gamma_rate, epsilon_rate = determineGammaAndEpislonRates(report)

    gamma_decimal = functools.reduce(lambda x, y: 2 * x + y, gamma_rate)
    epsilon_decimal = functools.reduce(lambda x, y: 2 * x + y, epsilon_rate)

    return gamma_decimal * epsilon_decimal

def verifyLifeSupportRating(report):

    o2_rules = np.copy(report)
    co2_rules = np.copy(report)

    for col in range(report.shape[1]):

        if o2_rules.shape[0] > 1:
            most_common_bit = 1 if np.sum(o2_rules[:,col]) >= (o2_rules.shape[0] / 2) else 0
            o2_rules = o2_rules[np.where(o2_rules[:,col] == most_common_bit)[0],:]

        if co2_rules.shape[0] > 1:
            least_common_bit = 0 if np.sum(co2_rules[:,col]) >= (co2_rules.shape[0] / 2) else 1
            co2_rules = co2_rules[np.where(co2_rules[:,col] == least_common_bit)[0],:]

    o2 = functools.reduce(lambda x, y: 2 * x + y, o2_rules[0,:])
    co2 = functools.reduce(lambda x, y: 2 * x + y, co2_rules[0,:])

    return o2 * co2

if __name__ == "__main__":

    # Get and Parse Input
    input = aocd.get_data(day = 3, year = 2021)
    report = []
    for line in input.split("\n"):
        binary = []
        for char in line.strip():
            binary += [int(char)]
        report += [binary]
    report = np.array(report)

    # Part 1
    print(getPowerConsumption(report))

    # Part 2
    print(verifyLifeSupportRating(report))