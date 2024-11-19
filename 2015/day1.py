import aocd
import os
    
def run_elevator(source):
    
    floor = 0
    for char in source:
        if char == "(":
            floor += 1
        else:
            floor -= 1
    
    return floor

def first_basement(input):
    
    floor = 0
    for i, char in enumerate(input):
        if char == "(":
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            return i + 1

if __name__ == "__main__":
    
    input = aocd.get_data(day = 1, year = 2015)
    print(run_elevator(input))
    print(first_basement(input))
