from functools import reduce, cache
import aocd
import numpy as np
import re

def parse_input(input):

    mirrors = []
    mirror_lines = []
    for line in input.split("\n"):
        if line == "":
            mirrors += ["\n".join(mirror_lines)]
            mirror_lines = []
        else:
            mirror_lines += [line.strip()]

    if mirror_lines:
        mirrors += ["\n".join(mirror_lines)]
    
    return mirrors

def find_reflection(mirror, ignore = None):

    mirror = np.array([re.split("", line)[1:-1] for line in mirror.split("\n") if line != ""])

    r, c = mirror.shape

    for i in range(1, r):
        if np.all(mirror[i - 1,:] == mirror[i,:]):
            result = "row", i
            if is_reflection(mirror, "horizontal", i) and result != ignore:
                return result
    
    for i in range(1, c):
        if np.all(mirror[:,i - 1] == mirror[:,i]):
            result = "column", i
            if is_reflection(mirror, "vertical", i) and result != ignore:
                return result

    return None

def find_reflection_smudge(mirror):

    original_reflection = find_reflection(mirror)

    for i, char in enumerate(mirror):
       if char in ["#", "."]:
            chars = list(mirror)
            chars[i] = "." if char == "#" else "#"
            reflection = find_reflection("".join(chars), ignore = original_reflection)
            if reflection is not None:
                return reflection        

    raise Exception("No reflection found")

def is_reflection(mirror, orientation, starting_index):

        if orientation not in ["horizontal", "vertical"]:
            raise TypeError(f"Unknown orientation {orientation}")

        if orientation == "vertical":
            steps = min(mirror.shape[1] - starting_index, starting_index)
        else:
            steps = min(mirror.shape[0] - starting_index, starting_index)

        for step in range(steps):

            left_index = starting_index - 1 - step
            right_index = starting_index + step

            if orientation == "vertical":
                left = mirror[:, left_index]
                right = mirror[:, right_index]
            elif orientation == "horizontal":
                left = mirror[left_index, :]
                right = mirror[right_index, :]

            if np.any(left != right): return False 

        return True


if __name__ == "__main__":

    mirrors = parse_input(aocd.get_data(day = 13, year = 2023))

    print(reduce(lambda acc, result: acc + (100 * result[1] if result[0] == "row" else result[1]), map(find_reflection, mirrors), 0))
    print(reduce(lambda acc, result: acc + (100 * result[1] if result[0] == "row" else result[1]), map(find_reflection_smudge, mirrors), 0))