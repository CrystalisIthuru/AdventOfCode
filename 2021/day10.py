import aocd
import functools

EXAMPLE="""
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip()

AUTOCOMPLETE_SCORES = {
    ")" : 1,
    "]" : 2,
    "}" : 3,
    ">" : 4
}

CORRUPTED_SCORES = {
    ")" : 3,
    "]" : 57,
    "}" : 1197,
    ">" : 25137
}

def eval_line(line):
    
    oppairs = {
        "}" : "{",
        "]" : "[",
        ")" : "(",
        ">" : "<"
    }

    opstack = []
    for op in line:
        if op in "[{(<":
            opstack += [op]
        elif op in "]})>":
            pair = oppairs[op]
            if opstack[-1] != pair:
                return "corrupted", opstack, op
            else:
                opstack = opstack[:-1]
        else:
            raise Exception(f"Unknown op, '{op}'")
    
    if len(opstack) == 0:
        return "success", None, None
    else:
        return "incomplete", opstack, None

def score_corrupted_lines(lines):

    oppairs = {
        "}" : "{",
        "]" : "[",
        ")" : "(",
        ">" : "<"
    }

    score = 0
    for line in lines:

        status, opstack, final_op = eval_line(line)
        if status == "corrupted":
            score += CORRUPTED_SCORES[final_op]
    
    return score

def score_incomplete_lines(lines):

    oppairs = {
        "{" : "}",
        "[" : "]",
        "(" : ")",
        "<" : ">"
    }

    scores = []
    for line in lines:
        status, opstack, final_op = eval_line(line)
        if status == "incomplete":
            scores += [functools.reduce(lambda acc, op: acc * 5 + AUTOCOMPLETE_SCORES[oppairs[op]], reversed(opstack), 0)]

    return sorted(scores)[len(scores) // 2]

if __name__ == "__main__":

    input = aocd.get_data(day = 10, year = 2021)
    lines = [line.strip() for line in input.split("\n")]

    # Part 1
    print(score_corrupted_lines(lines))

    # Part 2
    print(score_incomplete_lines(lines))