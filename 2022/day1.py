import aocd

if __name__ == "__main__":

    elves = []
    current_calories = 0
    for line in aocd.get_data(day = 1, year = 2022).split("\n"):
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
