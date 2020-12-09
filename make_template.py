import sys
import os

day = sys.argv[1]
template = f"""
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
        # .line_tokens(sep = "\\n", line_sep = "\\n\\n")
)

def solve(input):
    return None, None

answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {{answer1}}")
# print(submit({day}, 1, answer1).text)

print("Part 2")
print(f"Answer: {{answer2}}")
# print(submit({day}, 2, answer1).text)
"""

if not os.path.exists(day):
    os.makedirs(day)
with open(f"{day}/run.py", 'w') as f:
    f.write(template)