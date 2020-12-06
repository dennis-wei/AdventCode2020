
import os, sys
from re import split
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, submit
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

input = [r.replace("\n", " ").split() for r in raw_input.split("\n\n")]

def part1_row(inp):
    res = reduce(lambda x, y: x.union(y), inp, set())
    return res

def part1(full_input):
    return sum(len(part1_row(row)) for row in full_input)


answer1 = part1(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(6, 1, answer1).text)

def part2_row(inp):
    res = reduce(lambda x, y: Counter(x) + Counter(y), inp, Counter())
    return set(k for k, v  in res.items() if v == len(inp))

def part2(full_input):
    return sum(len(part2_row(row)) for row in full_input)

answer2 = part2(input)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(6, 2, answer1).text)
