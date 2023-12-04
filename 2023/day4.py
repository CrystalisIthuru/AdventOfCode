import os
import re

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "4.dat")

def score_scratchcard(card):

    match = re.match(r"Card\s*\d+:\s+((?:\d+\s+)+)\|\s+((?:\d+\s*)+)", card)

    winning_numbers = set([int(el) for el in re.split(r"\s+", match.group(1)) if el.strip() != ""])
    numbers = [int(el) for el in re.split(r"\s+", match.group(2)) if el.strip() != ""]

    winning_count = len([number for number in numbers if number in winning_numbers])

    if winning_count > 0:
        return 2 ** (winning_count - 1)
    else:
        return 0

def score_scratchcard_expanded(cards):

    card_library = {}
    card_queue = {}
    for card in cards:
        match = re.match(r"Card\s*(\d+):\s+((?:\d+\s+)+)\|\s+((?:\d+\s*)+)", card)
        
        card_id = int(match.group(1))
        card_winning_numbers = set([int(number) for number in re.findall(r"\d+", match.group(2))])
        card_numbers = [int(number) for number in re.findall(r"\d+", match.group(3))]

        card_library[card_id] = (card_winning_numbers, card_numbers)
        card_queue[card_id] = 1

    for card_id, count in card_queue.items():

        card_winning_numbers, card_numbers = card_library[card_id]
        winning_count = sum([1 for number in card_numbers if number in card_winning_numbers])
        next_ids = [i for i in range(card_id + 1, card_id + winning_count + 1) if i in card_library]

        for id in next_ids:
            card_queue[id] += count

    return sum(card_queue.values())

    #card_count = 0
    #card_queue = [2]
    #while len(card_queue) > 0:

    #    card_id = card_queue.pop(0)
    #    card_winning_numbers, card_numbers = card_library[card_id]

    #    winning_count = sum([1 for number in card_numbers if number in card_winning_numbers])

    #    card_queue += [i for i in range(card_id + 1, card_id + winning_count + 1) if i in card_library]
    #    card_count += 1

    #return card_count

if __name__ == "__main__":

    with open(INPUT_FILE, "r") as f:
        cards = f.readlines()

    print(sum([score_scratchcard(card) for card in cards]))
    print(score_scratchcard_expanded(cards))