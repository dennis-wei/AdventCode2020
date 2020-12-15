
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
        .lines()
        # .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

def update_turn_list(orig_list, update):
    if len(orig_list) == 0:
        return [update]
    elif len(orig_list) == 1:
        return orig_list + [update]
    else:
        return [orig_list[1], update]

def solve(input, size):
    nums = [int(n) for n in input[0].split(",")]
    last_turns_spoken = defaultdict(list)
    curr_turn = 1
    is_in_starter = True
    prev_word = None
    while curr_turn <= size:
        if is_in_starter:
            prev_word = nums.pop(0)
            last_turns_spoken[prev_word] = update_turn_list(last_turns_spoken[prev_word], curr_turn)
            if len(nums) == 0:
                is_in_starter = False
        else:
            if len(last_turns_spoken[prev_word]) == 1:
                prev_word = 0
                last_turns_spoken[0] = update_turn_list(last_turns_spoken[0], curr_turn)
            else:
                last_last_turn, last_turn = last_turns_spoken[prev_word]
                update = last_turn - last_last_turn
                last_turns_spoken[update] = update_turn_list(last_turns_spoken[update], curr_turn)
                prev_word = update

        curr_turn += 1

    return prev_word

answer1 = solve(input, 2020)
answer2 = solve(input, 30000000)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(15, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(15, 2, answer1).text)
