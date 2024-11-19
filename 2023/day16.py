import aocd
import numpy as np
from copy import deepcopy

def parse_input(input):

    return np.array([[char for char in line.strip()] for line in input.split("\n") if len(line.strip()) > 0])
    
def get_next_beam_location(location, direction):

    i, j = location

    if direction == "up":
        return i - 1, j
    elif direction == "down":
        return i + 1, j
    elif direction == "left":
        return i, j - 1
    else:
        return i, j + 1

def count_energized_tiles(contraption, starting_location, starting_direction):

    queue = [(starting_location, starting_direction)]
    marks = np.zeros_like(contraption, dtype = bool)

    visited = set()

    while queue:
    
        beam_location, direction = queue.pop(0)
        i, j = beam_location

        if (beam_location, direction) in visited: continue
        if i < 0 or i >= contraption.shape[0] or j < 0 or j >= contraption.shape[1]: continue

        marks[beam_location] = True
        visited.add((beam_location, direction))
        current_space = contraption[beam_location]
    
        if current_space == "|" and direction in ["left", "right"]:
            queue += [
                (get_next_beam_location(beam_location, "up"), "up"),
                (get_next_beam_location(beam_location, "down"), "down")
            ]
        elif current_space == "-" and direction in ["up", "down"]:
            queue += [
                (get_next_beam_location(beam_location, "left"), "left"),
                (get_next_beam_location(beam_location, "right"), "right")
            ]
        elif current_space == "\\": 
            if direction == "right":
                queue += [(get_next_beam_location(beam_location, "down"), "down")]
            elif direction == "left":
                queue += [(get_next_beam_location(beam_location, "up"), "up")]
            elif direction == "up":
                queue += [(get_next_beam_location(beam_location, "left"), "left")]
            else:
                queue += [(get_next_beam_location(beam_location, "right"), "right")] 
        elif current_space == "/":
            if direction == "right":
                queue += [(get_next_beam_location(beam_location, "up"), "up")]
            elif direction == "left":
                queue += [(get_next_beam_location(beam_location, "down"), "down")]
            elif direction == "up":
                queue += [(get_next_beam_location(beam_location, "right"), "right")] 
            else:
                queue += [(get_next_beam_location(beam_location, "left"), "left")]
     
        else: # "." or pass through for "|" and "-"
            queue += [(get_next_beam_location(beam_location, direction), direction)]

    return np.sum(marks)

def count_best_energized_tiles(contraption):

    indices = np.indices(contraption.shape)

    top_row = indices[:,0,:]
    bot_row = indices[:,-1,:]
    left_col = indices[:,:,0]
    right_col = indices[:,:,-1]

    edges = [top_row, bot_row, left_col, right_col]
    directions = ["down", "up", "right", "left"]

    max_energized = 0
    for edge, direction in zip(edges, directions):
        for i in range(edge.shape[1]):
            energized_tiles = count_energized_tiles(contraption, tuple(edge[:,i]), direction)
            max_energized = max(max_energized, energized_tiles)

    return max_energized

if __name__ == "__main__":

    contraption = parse_input(aocd.get_data(day = 16, year = 2023))
    print(count_energized_tiles(contraption, (0, 0), "right"))
    print(count_best_energized_tiles(contraption))
