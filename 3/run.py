import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, submit

parser = argparse.ArgumentParser()
parser.add_argument("--from-std-in", action='store_true', default=False)
args = parser.parse_args()
if args.from_std_in:
    raw_input = split_newline(clipboard.paste())
else:
    with open("input.txt", "r") as f:
        raw_input = [l.strip() for l in f]
if raw_input[-1] == "":
    raw_input = raw_input[:-1]

trees = 0
for row_number, row in enumerate(raw_input):
    col_number = row_number * 3
    char = row[col_number % len(row)]
    if char == '#':
        trees += 1

answer1 = trees 

print("Part 1")
print(f"Answer: " + str(answer1))
print(submit(3, 1, answer1).text)


print("Part 2")
total_product = 1
for right, down in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    trees = 0
    for row_number, row in enumerate(raw_input):
        if row_number % down != 0:
            continue
        col_number = row_number * right // down
        char = row[col_number % len(row)]
        if char == '#':
            trees += 1
    print(f"{right}, {down} | {trees}")
    total_product *= trees

answer2 = total_product
print(f"Answer: " + str(answer2))
print(submit(3, 2, answer1).text)
