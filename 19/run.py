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

import nltk

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
        .all()
        # .ints()
        # .int_tokens()
        # .tokens()
        # .lines()
        # .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

def solve_nltk(input):
    nltk_grammar_str = input.split("\n\n")[0].replace(":", " ->")
    grammar = nltk.CFG.fromstring(nltk_grammar_str)
    print(grammar)
    parser = nltk.ChartParser(grammar)

    acc1 = 0
    for sentence in input.split("\n\n")[1].split("\n"):
        # print(sentence)
        num_matches = 0
        for tree in parser.parse(sentence):
            num_matches += 1
        if num_matches > 0:
            acc1 += 1

    return acc1

start = time.time()
answer1 = solve_nltk(input)

input2 = input.replace("8: 42\n", "8: 42 | 42 8\n").replace("11: 42 31\n", "11: 42 31 | 42 11 31\n")
answer2 = solve_nltk(input2)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(19, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(19, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")