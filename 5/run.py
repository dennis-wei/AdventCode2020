import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, submit
from math import floor, ceil

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

def get_seat(row, col):
    return row * 8 + col

def do_binary(char, lo, hi):
    if char == "F" or char == "L":
        return lo, floor((lo + hi) / 2)
    elif char == "B" or char == "R":
        return ceil((lo + hi) / 2) , hi
    
def fast_binary(s):
    return int(s.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), 2)

def get_seat_id(s):
    return fast_binary(s)

def handle_str(s):
    lo, hi = 0, 127
    for c in s[:7]:
        lo, hi = do_binary(c, lo, hi)
    if not lo == hi:
        print(lo, hi, "row error")
    
    row = lo

    lo, hi = 0, 7
    for c in s[7:]:
        lo, hi = do_binary(c, lo, hi)
    if not lo == hi:
        print(s[7:], lo, hi, "col error")

    col = lo
    return row, col

max_id = max(get_seat_id(inp) for inp in raw_input)
answer1 = max_id

print("Part 1")
print(f"Answer: {answer1}")

answer2 = None

taken_seats = set(get_seat_id(inp) for inp in raw_input)
for s in taken_seats:
    if s + 2 in taken_seats and s + 1 not in taken_seats:
        answer2 = s + 1
        break

print("Part 2")
print(f"Answer: {answer2}")
