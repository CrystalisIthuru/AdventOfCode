import aocd
import re

def parse_input():

    input = aocd.get_data(day = 2, year = 2015)    
    dimensions = []
    for line in [line.strip() for line in input.split("\n")]:
        dimensions += [tuple(map(lambda x: int(x), re.findall(r"\d+", line)))]
            
    return dimensions

def area_of_smallest_side(l, w, h):
    
    a, b = sorted([l, w, h])[:2]
    return a * b

def cubic_volumn(l, w, h):
    
    return l * w * h

def smallest_perimeter(l, w, h):
    
    a, b = sorted([l, w, h])[:2]
    return a * 2 + b * 2

def surface_area(l, w, h):
    
    return 2 * l * w + 2 * w * h + 2 * h * l

def total_wrapping_paper(dimensions):
    
    return sum(map(lambda x: surface_area(*x) + area_of_smallest_side(*x), dimensions))

def total_ribbon(dimensions):
    
    return sum(map(lambda x: smallest_perimeter(*x) + cubic_volumn(*x), dimensions))

if __name__ == "__main__":
    
    dimensions = parse_input()
    print(total_wrapping_paper(dimensions))
    print(total_ribbon(dimensions))