import numpy as np
import os
import re

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "6.dat")

def turn_on_lights(instructions):
    
    lights = np.zeros((1000, 1000), dtype = bool)
    
    for command, top_left, bot_right in instructions:
        
        lx, ly = top_left
        rx, ry = bot_right
        
        if command == "on":
            lights[lx:rx+1,ly:ry+1] = True
        elif command == "off":
            lights[lx:rx+1,ly:ry+1] = False
        elif command == "toggle":
            lights[lx:rx+1,ly:ry+1] = np.logical_not(lights[lx:rx+1,ly:ry+1])
        else:
            raise Exception(f"Unknown command '{command}")
        
    return lights

def increase_brightness(instructions):
    
    lights = np.zeros((1000, 1000))

    for command, (lx, ly), (rx, ry) in instructions:
         
        if command == "off":
            lights[lx:rx+1,ly:ry+1] -= 1
            lights[np.where(lights < 0)] = 0
        elif command == "on":
            lights[lx:rx+1,ly:ry+1] += 1
        elif command == "toggle":
            lights[lx:rx+1,ly:ry+1] += 2
        else:
            raise Exception(f"Unknown command '{command}")

    return int(np.sum(lights))
            
def parse_input(input_file):
    
    instructions = []
    with open(input_file, "r") as f:
        for line in f:
            match = re.match("(toggle|turn (on|off)) (\d+),(\d+) through (\d+),(\d+)", line)
            
            if "turn" in match.group(1):
                value = match.group(2)
            else:
                value = match.group(1)
            
            top_left = int(match.group(3)), int(match.group(4))
            bot_right = int(match.group(5)), int(match.group(6))
            
            instructions += [(value, top_left, bot_right)]
            
    return instructions

if __name__ == "__main__":
    
    instructions = parse_input(INPUT_FILE)
    print(np.sum(turn_on_lights(instructions)))
    #instructions = [("toggle", (0, 0), (999, 999))]
    print(increase_brightness(instructions))