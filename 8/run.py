
import os, sys
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
raw_input = raw_input.strip()

input = raw_input

def step(row_num, acc, row):
    try:
        op, args = row.split(" ")
    except:
        print("malformed row: ", row)
        sys.exit(1)
    num = int(args)
    if op == "jmp":
        return row_num + num, acc
    elif op == "acc":
        return row_num + 1, acc + num
    elif op == "nop":
        return row_num + 1, acc

def run_program(rows):
    acc = 0
    row_num = 0

    encountered = set()
    nop_jmp_backtrace = deque()

    is_valid_program = True
    while row_num < len(rows):
        if row_num in encountered:
            is_valid_program = False
            break
        encountered.add(row_num)
        if "nop" in rows[row_num] or "jmp" in rows[row_num]:
            nop_jmp_backtrace.appendleft(row_num)
        row_num, acc = step(row_num, acc, rows[row_num])
    
    return acc, is_valid_program, nop_jmp_backtrace

def solve(input):
    rows = input.split("\n")

    answer1, _, backtrace = run_program(rows)
    
    print("backtrace: ", backtrace)

    result = None
    for viable_row_num in backtrace:
        initial_row = rows[viable_row_num]
        modified_rows = rows.copy()
        if "jmp" in initial_row:
            modified_rows[viable_row_num] = initial_row.replace("jmp", "nop")
        else:
            modified_rows[viable_row_num] = initial_row.replace("nop", "jmp")

        result, is_valid, _ = run_program(modified_rows)
        if is_valid:
            print(f"modified row: #{viable_row_num} | original: {initial_row} | modified: {modified_rows[viable_row_num]}")
            break

    return answer1, result

answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(8, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(8, 2, answer1).text)
