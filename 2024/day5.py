import aocd
import numpy as np
import re

EXAMPLE = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".strip()

def is_correctly_ordered(rules, pages):

    order = { page : i for i, page in enumerate(pages) }

    for left, right in rules:
        if left in order and right in order and order[left] >= order[right]:
            return False
    else:
        return True
    
def order_correctly(rules, pages):

    order = { page : i for i, page in enumerate(pages) }

    while True:
        for left, right in rules:
            if left in order and right in order and order[left] >= order[right]:
                temp = order[left]
                order[left] = order[right]
                order[right] = temp
                break
        else:
            break

    order = { v : k for k, v in order.items() }
    return [order[i] for i in range(len(pages))]

if __name__ == "__main__":

    input = aocd.get_data(day = 5, year = 2024)

    # Parse Input
    rules = []
    pages = []
    parsing_rules = True
    for line in input.split("\n"):
        line = line.strip()

        if not line:
            parsing_rules = False
            continue
            
        if parsing_rules:
            rules +=[[int(el) for el in re.findall(r"\d+", line)]]
        else:
            pages += [[int(el) for el in re.findall(r"\d+", line)]]

    # Part 1
    count = 0
    for set in pages:
        if is_correctly_ordered(rules, set):
            mid = len(set) // 2
            count += set[mid]
    print(count)

    # Part 2
    count = 0
    for set in pages:
        if not is_correctly_ordered(rules, set):
            set = order_correctly(rules, set)
            mid = len(set) // 2
            count += set[mid]
    print(count)
