from functools import reduce, cmp_to_key
import os
import re
import enum
import numpy as np

INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "inputs")
INPUT_FILE = os.path.join(INPUT_DIRECTORY, "7.dat")

class HAND_TYPES(enum.IntEnum):

    FIVE = 5,
    FOUR = 4,
    FULL = 3,
    THREE = 2,
    TWO = 1,
    ONE = 0,
    HIGH = -1

def parse_input(input_file):

    hands = []
    bids = []
    with open(input_file, "r") as f:

        for line in f:

            if line.strip() == "": continue

            hand, bid = [el for el in re.split(r"\s+", line) if len(el) != 0]
            hands += [hand]
            bids += [int(bid)]

    return hands, bids

def convert_jokers(hand):

    if "J" not in hand: return hand
    if hand == "JJJJJ": return "AAAAA"

    replace_char = None
    char_counts = {}
    for char in hand:
        if char == "J":
            continue
        
        if char not in char_counts: char_counts[char] = 0
        char_counts[char] += 1

        if replace_char is None:
            replace_char = char
            continue

        if char_counts[char] > char_counts[replace_char]:
            replace_char = char
        elif char_counts[char] == char_counts[replace_char] and get_card_value(char) > get_card_value(replace_char):
            replace_char = char

    return hand.replace("J", replace_char)

def get_card_value(card, use_jokers = False):
    
    face_map = {
        "A" : 14,
        "K" : 13,
        "Q" : 12,
        "J" : 11,
        "T" : 10
    }
    if use_jokers: face_map["J"] = 1

    if card in face_map:
        return face_map[card]
    else:
        return int(card)


def get_hand_values(hand, use_jokers = False):

    return [get_card_value(card, use_jokers) for card in hand]

def get_hand_type(hand, use_jokers = False):

    if use_jokers: hand = convert_jokers(hand)

    hand = np.array([ch for ch in hand])
    unique, counts = np.unique(hand, return_counts = True)

    if unique.size == 1:
        return HAND_TYPES.FIVE
    elif unique.size == 2:
        if counts[0] in [1, 4]:
            return HAND_TYPES.FOUR
        elif counts[0] in [3, 2]:
            return HAND_TYPES.FULL
    elif unique.size == 3:
        if any(counts == 3):
            return HAND_TYPES.THREE
        else:
            return HAND_TYPES.TWO
    elif unique.size == 4:
        return HAND_TYPES.ONE
    else:
        return HAND_TYPES.HIGH

def compare_hands(left, right, use_jokers = False):

    left_hand_type = get_hand_type(left, use_jokers)
    right_hand_type = get_hand_type(right, use_jokers)

    if left_hand_type == right_hand_type:
        left_values = get_hand_values(left, use_jokers)
        right_values = get_hand_values(right, use_jokers)
        for left_val, right_val in zip(left_values, right_values):
            if left_val == right_val:
                continue
            elif left_val < right_val:
                return -1
            elif left_val > right_val:
                return 1
        else:
            return 0
    else:
        if left_hand_type < right_hand_type:
            return -1
        elif left_hand_type > right_hand_type:
            return 1
        else:
            return 0

def calculate_winnings(hands, bids, use_jokers = False):

    
    ordered = sorted(zip(hands, bids), key = cmp_to_key(lambda x, y: compare_hands(x[0], y[0], use_jokers)))

    winnings = 0
    for i, (hand, bid) in enumerate(ordered):
        winnings += bid * (i + 1)

    return winnings

if __name__ == "__main__":

    hands, bids = parse_input(INPUT_FILE)
    print(calculate_winnings(hands, bids))
    print(calculate_winnings(hands, bids, use_jokers = True))

