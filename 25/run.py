from re import sub
import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import get_all_nums, submit, Input, Grid
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
        .ints()
        # .int_tokens()
        # .tokens()
        # .lines()
        # .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

def solve(input):
    key1 = input[0]
    key2 = input[1]
    
    cached = defaultdict(lambda: {0: 1})

    def transform(loop_size, subject_number = 7, use_cache = True):
        if use_cache:
            if loop_size in cached[subject_number]:
                return cached[subject_number][loop_size]
            value = (cached[subject_number][loop_size - 1] * subject_number) % 20201227
            cached[subject_number][loop_size] = value
            return value
        else:
            value = 1
            for i in range(loop_size):
                value = (value * subject_number) % 20201227
            return value
    
    def get_loop_number(input):
        loop_size = 1
        while transform(loop_size) != input:
            if loop_size % 1000000 == 0:
                print(f"upping loop_size from {loop_size}")
            loop_size += 1
        return loop_size
        
    pkey1 = get_loop_number(key1)
    pkey2 = get_loop_number(key2)

    print(pkey1, pkey2)

    return transform(pkey2, key1, use_cache=False), None

start = time.time()
# input = [5764801, 17807724]
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(25, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(25, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")