import aocd
import re
import functools

SHORT_EXAMPLE = """
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
"""

EXAMPLE = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

def solve_wires(inputs, outputs):

    # Find the wires that display the digets 1, 4, 7, and 8 
    # since those are the only digets that use 2, 4, 3, and 7
    # signals respectfully, to display.
    one = None
    four = None
    seven = None
    eight = None
    for n in inputs:
        if len(n) == 2:
            one = set([char for char in n])
        elif len(n) == 4:
            four = set([char for char in n])
        elif len(n) == 3:
            seven = set([char for char in n])
        elif len(n) == 7:
            eight = set([char for char in n])

    # Count the simple values
    count = 0
    for output in [set([char for char in n]) for n in outputs]:
        if output == one or output == four or output == seven or output == eight:
            count += 1

    six_signal_numbers = [set([char for char in n]) for n in inputs if len(n) == 6]
    five_signal_numbers = [set([char for char in n]) for n in inputs if len(n) == 5]

    # Deduce the original wires using set algebra
    a = seven - one
    eg = eight - seven - four
    bd = four - one
    nine = [n for n in six_signal_numbers if len(n - four - a) == 1][0]
    g = nine - four - a
    e = eg - g
    five = [n for n in five_signal_numbers if len(nine - n - one) == 0][0]
    two = [n for n in five_signal_numbers if len(nine - n) == 2][0]
    three = [n for n in five_signal_numbers if len(nine - n) == 1 and n != five][0]

    six = five | e
    b = five - two - one
    d = four - one - b
    zero = eight - d
 
    decoder = [zero, one, two, three, four, five, six, seven, eight, nine]
    numbers = []
    for output in outputs:
        output = set([char for char in output])
        for i, number in enumerate(decoder):
            if output == number:
                numbers += [i]
                break
        else:
            raise Exception(f"Could not decode {output} with {decoder}")
    number = functools.reduce(lambda acc, x: acc * 10 + x, numbers)

    return count, number

if __name__ == "__main__":

    input = aocd.get_data(day = 8, year = 2021)

    # Parse input
    patterns = []
    for line in input.split("\n"):
        if line.strip() == "": continue
        split = re.findall(r"[a-z]+", line)
        patterns += [(split[:-4], split[-4:])]
    
    # Part 1
    print(sum([solve_wires(input, output)[0] for input, output in patterns]))

    # Part 2
    print(sum([solve_wires(input, output)[1] for input, output in patterns]))