import aocd
import numpy as np

EXAMPLE = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".strip()

def check_direction(wordsearch, word, x, y, move):

    check = []
    for it in range(len(word)):
        i = x + move[0] * it
        j = y + move[1] * it

        if i < 0 or i >= wordsearch.shape[0] or j < 0 or j >= wordsearch.shape[1]:
            return False
        
        check += [wordsearch[i, j]]
    
    check = "".join(check)
    return word == check 

def find_and_count(wordsearch, word):

    count = 0
    for (i, j), el in np.ndenumerate(wordsearch):
        if el == word[0]:

            count += check_direction(wordsearch, word, i, j, (1, 0))   # Down
            count += check_direction(wordsearch, word, i, j, (-1, 0))  # Up
            count += check_direction(wordsearch, word, i, j, (0, 1))   # Right
            count += check_direction(wordsearch, word, i, j, (0, -1))  # Left
            count += check_direction(wordsearch, word, i, j, (1, 1))   # Down-Right
            count += check_direction(wordsearch, word, i, j, (-1, 1))  # Up-Right
            count += check_direction(wordsearch, word, i, j, (-1, -1)) # Down-Left
            count += check_direction(wordsearch, word, i, j, (1, -1))  # Up-Left

    return count

def find_and_count_cross(wordsearch):

    count = 0
    for (i, j), el in np.ndenumerate(wordsearch):
        if el == "A":

            min_x = max(0, i - 1)
            min_y = max(0, j - 1)
            max_x = min(i + 1, wordsearch.shape[1] - 1)
            max_y = min(j + 1, wordsearch.shape[1] - 1)

            block = wordsearch[min_x:max_x+1,min_y:max_y+1]
            if block.shape != (3, 3):
                continue            

            if (check_direction(block, "MAS", 0, 0, (1, 1)) or check_direction(block, "SAM", 0, 0, (1, 1))) and \
               (check_direction(block, "MAS", 0, 2, (1, -1)) or check_direction(block, "SAM", 0, 2, (1, -1))):
                count += 1

    return count

if __name__ == "__main__":

    input = EXAMPLE
    input = aocd.get_data(day = 4, year = 2024)
    wordsearch = np.array([[char for char in line.strip()] for line in input.split("\n")])

    # Part 1
    print(find_and_count(wordsearch, "XMAS"))

    # Part 2
    print(find_and_count_cross(wordsearch))
        