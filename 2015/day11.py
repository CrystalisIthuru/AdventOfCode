import aocd

def generate_new_password(password):

    current_password = increment_password(password)
    while not is_valid_password(current_password):
        current_password = increment_password(current_password)
    return current_password

def has_increasing_straight(password):

    ascii_values = [ord(char) for char in password]
    
    count = 1
    prev = ascii_values[0]
    for current in ascii_values[1:]:
        if count == 3:
            return True
        
        if current == prev + 1:
            count += 1
        else:
            count = 1

        prev = current

    return count >= 3

def has_two_non_overlapping_pairs(password):

    count = 0
    prev = ""
    for char in password:

        if char == prev:
            prev = ""
            count += 1
        else:
            prev = char

    return count >= 2

def increment_password(password):

    ascii_values = list(reversed([ord(char) for char in password]))

    new_password = []
    for i, value in enumerate(ascii_values):
        next_value = value + 1
        if next_value > 122:
            new_password += [97]
        else:
            new_password += [next_value] + ascii_values[i + 1:]
            break
    
    return "".join(reversed([chr(value) for value in new_password]))

def is_valid_password(password):

    if "i" in password or "o" in password or "l" in password:
        return False
    
    return has_increasing_straight(password) and has_two_non_overlapping_pairs(password)


if __name__ == "__main__":

    input = aocd.get_data(day = 11, year = 2015)

    print(generate_new_password(input))
    print(generate_new_password(generate_new_password(input)))