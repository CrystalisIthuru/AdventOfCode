import aocd
import numpy as np
import re

EXAMPLE = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

class BingoBoard:

    def __init__(self, board):

        self.board = board
        self.marks = np.zeros_like(board, dtype = bool)

    def __repr__(self):

        return "Board:\n" + repr(self.board) + "\nMarks:\n" + repr(self.marks)

    def mark(self, n):

        index = np.argwhere(self.board == n)
        if index.size > 0:
            self.marks[index[:,0], index[:,1]] = True

        return np.any(np.sum(self.marks, axis = 0) == 5) or np.any(np.sum(self.marks, axis = 1) == 5)
    
    def score(self, last_draw):

        score = np.copy(self.board)
        score[np.where(self.marks)] = 0
        return np.sum(score) * last_draw
            
def run_bingo(draw_numbers, boards, win_first = True):

    winning_boards = np.zeros((len(boards),), dtype = bool)
    for draw in draw_numbers:
        for i, board in enumerate(boards):
            if board.mark(draw):
                if win_first:
                    return board.score(draw)
                else:
                    winning_boards[i] = True
                    if np.sum(winning_boards) == len(boards):
                        return board.score(draw)

if __name__ == "__main__":

    #input = EXAMPLE
    input = aocd.get_data(day = 4, year = 2021)
    lines = [line for line in input.split("\n") if len(line.strip()) > 0]

    draw_numbers = [int(n) for n in lines[0].strip().split(",")]
    bingo_boards = []
    for i in range(1, len(lines), 5):
        bingo_boards += [BingoBoard(np.array([
            [int(n) for n in re.split(r"\s+", lines[i + 0].strip())],
            [int(n) for n in re.split(r"\s+", lines[i + 1].strip())],
            [int(n) for n in re.split(r"\s+", lines[i + 2].strip())],
            [int(n) for n in re.split(r"\s+", lines[i + 3].strip())],
            [int(n) for n in re.split(r"\s+", lines[i + 4].strip())]
        ]))]

    # Part 1
    print(run_bingo(draw_numbers, bingo_boards))

    # Part 2
    print(run_bingo(draw_numbers, bingo_boards, False))

