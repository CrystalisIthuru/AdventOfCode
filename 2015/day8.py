import aocd

def parse_input(input):

    strings = []
    for line in input.split("\n"):
        line = line.strip()
        strings += [(line, eval(line))]
    
    return strings

def encoded_length(string):

    return len(string) + string.count("\\") + string.count("\"") + 2

if __name__ == "__main__":

    strings = parse_input(aocd.get_data(day = 8, year = 2015))
    print(sum(map(lambda string: len(string[0]) - len(string[1]), strings)))
    print(sum(map(lambda string: encoded_length(string[0]) - len(string[0]), strings)))