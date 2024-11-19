import aocd

def is_nice(str):
    
    vowel_count = 0
    has_double = False
    for i in range(len(str)):
        current_char = str[i]
       
        if is_vowel(current_char): vowel_count += 1
        if i == 0: continue
        
        prev_char = str[i - 1]
        if current_char == prev_char: has_double = True
        if prev_char + current_char in ["ab", "cd", "pq", "xy"]: return False
    
    return vowel_count >= 3 and has_double

def is_nice2(string):
    
    pairs = set()
    pair_queue = [string[:2]]
    
    has_repeat = False
    has_pair = False
    for i in range(2, len(string)):
        current_char = string[i]
        prev_char = string[i - 1]
        
        if prev_char + current_char in pairs: has_pair = True
        
        if pair_queue: pairs.add(pair_queue.pop(0))
        pair_queue += [prev_char + current_char]
        
        if current_char == string[i - 2]: has_repeat = True
            
    return has_repeat and has_pair
            
def is_vowel(char):

    return char in "aeiou"

def parse_input(input):
    
        return list(map(lambda x: x.strip(), input.split("\n")))

if __name__ == "__main__":
    
    strings = parse_input(aocd.get_data(day = 5, year = 2015))
    print(sum(map(lambda x: is_nice(x), strings)))
    print(sum(map(lambda x: is_nice2(x), strings)))
