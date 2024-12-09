import aocd
import json

EXAMPLE = '{"a":{"b":4},"c":-1}'
EXAMPLE2 = '[[[3]]]'

def sum_numbers(obj, ignore_red = False):

    if isinstance(obj, dict):
        result = 0
        for v in obj.values():
            if ignore_red and v == "red":
                return 0
            else:
                result += sum_numbers(v, ignore_red)
        return result
    elif isinstance(obj, list):
        result = 0
        for v in obj:
            result += sum_numbers(v, ignore_red)
        return result
    elif isinstance(obj, int):
        return obj
    else:
        return 0
    
if __name__ == "__main__":

    _in = aocd.get_data(year = 2015, day = 12)
    obj = json.loads(_in)

    # Part 1
    print(sum_numbers(obj))
    
    # Part 2
    print(sum_numbers(obj, ignore_red = True))
