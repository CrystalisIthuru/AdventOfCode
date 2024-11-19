import aocd
 
def move_direction(location, direction):
    
    x, y = location
    if direction == "^":
        return x - 1, y
    elif direction == "v":
        return x + 1, y
    elif direction == "<":
        return x, y - 1
    elif direction == ">":
        return x, y + 1
    else:
        raise TypeError(f"Unknown direction. '{direction}'")

def move_directions(directions):
    
    current_location = (0, 0)
    visited = set()
    for direction in directions:
        visited.add(current_location)
        current_location = move_direction(current_location, direction)
    
    return visited

def move_direction_robo(directions):
    
    current_location_santa = (0, 0)
    current_location_robo = (0, 0)
    visited = set([(0, 0)])
    for i, direction in enumerate(directions):
        if i % 2 == 0:
            current_location_santa = move_direction(current_location_santa, direction)
            visited.add(current_location_santa)
        else:
            current_location_robo = move_direction(current_location_robo, direction)
            visited.add(current_location_robo)
            
    return visited

if __name__ == "__main__":
    
    directions = aocd.get_data(day = 3, year = 2015)
    print(len(move_directions(directions)))
    #directions = "^v^v^v^v^v"
    print(len(move_direction_robo(directions)))
