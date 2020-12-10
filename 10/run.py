
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

def get_jumps(nums):
    sorted_nums = [0] + sorted(nums)
    print(sorted_nums[-1])
    sorted_nums.append(sorted_nums[-1] + 3)
    jumps = defaultdict(int)
    for i, num in enumerate(sorted_nums[1:]):
        jumps[num - sorted_nums[i]] += 1

    return jumps[1] * jumps[3]


def table_fill(nums):
    nums_set = set(nums)
    max_num = max(nums)
    table = {}

    table[0] = 1
    for i in range(1, max_num + 1):
        if i in nums_set:
            table[i] = table.get(i - 1, 0) + table.get(i - 2, 0) + table.get(i - 3, 0)
    return table[max_num]

def solve(input):
    result1 = get_jumps(input)
    result2 = table_fill(input)

    return result1, result2

answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(10, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(10, 2, answer1).text)
