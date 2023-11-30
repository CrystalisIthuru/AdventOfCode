import os
INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE_1 = os.path.join(INPUT_DIRECTORY, "1-1.dat")

if __name__ == "__main__":

    elves = []
    with open(INPUT_FILE_1, "r") as f:

        current_calories = 0
        for line in f:
            line = line.strip()
            
            if len(line) == 0:
                elves += [current_calories]
                current_calories = 0
            else:
                current_calories += int(line)

        elves += [current_calories]

    elves = sorted(zip(range(len(elves)), elves) , key = lambda x: x[1])
    print(elves[-1][1])
    print(sum([elf[1] for elf in elves[-3:]]))
