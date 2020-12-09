
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, submit, Input
from math import floor, ceil
from functools import reduce

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
        .ints()
        # .lines()
        # .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

def create_sliding_window(input, start, stop):
    return set(input[start:stop])

def pair_exists(target, window):
    for e in window:
        if target - e in window:
            return True
    return False


WINDOW_SIZE = 25
def solve(nums):
    part1 = None
    for i in range(WINDOW_SIZE, len(nums)):
        window = create_sliding_window(nums, i - WINDOW_SIZE, i)
        target = nums[i]
        if not pair_exists(target, window):
            part1 = target
            break

    start = 0
    stop = 1
    while True:
        sum_attempt = sum(nums[start:stop])
        if sum_attempt == part1:
            break
        elif sum_attempt < part1:
            stop += 1
        elif sum_attempt > part1:
            start += 1
    
    min_num = min(nums[start:stop])
    max_num = max(nums[start:stop])

    return part1, min_num + max_num

answer1, answer2 = solve(input)


print("Part 1")
print(f"Answer: {answer1}")
# print(submit(9, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(9, 2, answer1).text)
