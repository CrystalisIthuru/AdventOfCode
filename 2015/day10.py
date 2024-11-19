from functools import reduce
import aocd

def look_and_say(n):

    prev_char = str(n)[0]
    count = 1
    result = ""
    for char in str(n)[1:]:
        if char != prev_char:
            result += str(count) + prev_char
            count = 1
        else:
            count += 1
        prev_char = char 
    else:
        result += str(count) + prev_char

    return result

if __name__ == "__main__":

    n = aocd.get_data(day = 10, year = 2015)

    print(len(reduce(lambda acc, _: look_and_say(acc), range(40), n)))
    print(len(reduce(lambda acc, _: look_and_say(acc), range(50), n)))
