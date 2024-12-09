import aocd
import numpy as np
import re

EXAMPLE = "2333133121414131402"
EXAMPLE2 = "12345"

def optimize(files):

    files = [char for char in files]

    left = 0
    right = len(files) - 1

    while left < right:

        # Move to next empty block
        if files[left] != None:
            left += 1
            continue

        # Move to next non-empty block
        if files[right] == None:
            right -= 1
            continue

        files[left] = files[right]
        files[right] = None
        left += 1
        right -= 1

    return files

def optimize_no_frag(files):

    index = len(files) - 1
    while index >= 0:
        
        # Continue if file is empty block or file already moved
        if files[index].id < 0 or files[index].moved:
            index -= 1
            continue

        files[index].moved = True

        for i in range(index):

            if files[i].id < 0:

                if files[i].space == files[index].space:
                    temp = files[index]
                    files[index] = files[i]
                    files[i] = temp
                    index -= 1
                    break
                elif files[i].space > files[index].space:

                    spacer = FileBlockNoFrag(-1, files[i].space - files[index].space)

                    # Replace Index with empty space
                    temp = files[index]
                    files[index] = FileBlockNoFrag(-1, files[index].space)

                    # Replace current with index and spacer
                    files = files[:i] + [temp, spacer] + files[i + 1:]

                    break
        else:
            index -= 1

    return files

def checksum(files):
    result = 0
    for i, block in enumerate(files):
        if block is not None:
            result += i * block.id
    return result

def checksum_nofrag(files):

    index = 0
    result = 0
    for file in files:
        if file.id >= 0:
            for _ in range(file.space):
                result += index * file.id
                index += 1
        else:
            index += file.space
    
    return result

def visualize_nofrag(files):
    
    visual = ""
    for file in files:
        if file.id >=0:
            visual += str(file.id) * file.space
        else:
            visual += "." * file.space

    return visual


class FileBlock:

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return str(self.id)
    
class FileBlockNoFrag:

    def __init__(self, id, space):
        self.id = id
        self.space = space
        self.moved = False

if __name__ == "__main__":

    _in = aocd.get_data(year = 2024, day = 9)

    # Part 1
    files = []
    index = 0
    for i, char in enumerate(_in):
        if i % 2 == 0:
            files += [FileBlock(index) for _ in range(int(char))]
            index += 1
        else:
            files += [None for _ in range(int(char))]
    print(checksum(optimize(files)))

    # Part 2
    files = []
    index = 0
    for i, char in enumerate(_in):
        if int(char) > 0:
            if i % 2 == 0:
                files += [FileBlockNoFrag(index, int(char))]
                index += 1
            else:
                files += [FileBlockNoFrag(-1, int(char))]

    print(checksum_nofrag(optimize_no_frag(files)))