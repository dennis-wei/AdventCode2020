import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, submit, Input
from math import floor, ceil
from functools import reduce
from copy import deepcopy

parser = argparse.ArgumentParser()
parser.add_argument("--from-std-in", action='store_true', default=False)
args = parser.parse_args()
if args.from_std_in:
    raw_input = clipboard.paste()
else:
    with open("input.txt", "r") as f:
        raw_input = f.read()
raw_input = raw_input.strip()

input = (
    Input(raw_input)
        # .all()
        # .ints()
        # .int_tokens()
        # .tokens()
        # .lines()
        # .line_tokens()
        .line_tokens(sep = "\n", line_sep = "\n\n")
)

def parse_deck(input):
    deck = deque()
    for row in input[1:]:
        deck.append(int(row))
    
    return deck

def play_round(deck1, deck2):
    while len(deck1) > 0 and len(deck2) > 0:
        c1 = deck1.popleft()
        c2 = deck2.popleft()

        if c1 > c2:
            deck1.append(c1)
            deck1.append(c2)
        elif c2 > c1:
            deck2.append(c2)
            deck2.append(c1)
    
    if len(deck1) > 0:
        return 1, deck1
    else:
        return 2, deck2
    
def play_recursive_game(deck1, deck2, game_number):
    prior_decks = set()

    while len(deck1) > 0 and len(deck2) > 0:
        if (tuple(deck1), tuple(deck2)) in prior_decks:
            return 1, deck1
        
        prior_decks.add((tuple(deck1), tuple(deck2)))

        c1 = deck1.popleft()
        c2 = deck2.popleft()

        if len(deck1) >= c1 and len(deck2) >= c2:
            new_deck1 = deque(list(deck1)[:c1])
            new_deck2 = deque(list(deck2)[:c2])
            winner, _ = play_recursive_game(new_deck1, new_deck2, game_number + 1)
        
        else:
            if c1 > c2:
                winner = 1
            else:
                winner = 2
        
        if winner == 1:
            deck1.append(c1)
            deck1.append(c2)
        else:
            deck2.append(c2)
            deck2.append(c1)
    
    if len(deck1) > 0:
        return 1, deck1
    else:
        return 2, deck2


def solve(input):
    deck1 = parse_deck(input[0])
    deck2 = parse_deck(input[1])

    orig_deck1 = deepcopy(deck1)
    orig_deck2 = deepcopy(deck2)

    print("starting decks")
    print(list(deck1))
    print(list(deck2))

    winner1, winning_deck1 = play_round(deck1, deck2)
    print("Part 1 winner: ", winner1)

    acc = 0
    for i, c in enumerate(list(winning_deck1)[::-1]):
        acc += (i + 1) * c

    deck1 = orig_deck1
    deck2 = orig_deck2

    winner2, winning_deck2 = play_recursive_game(deck1, deck2, 0)
    print("Part 2 winner: ", winner2)

    acc2 = 0
    for i, c in enumerate(list(winning_deck2)[::-1]):
        acc2 += (i + 1) * c

    print()
    return acc, acc2

start = time.time()
game_number = 0
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(22, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(22, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")