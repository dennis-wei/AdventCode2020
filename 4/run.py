
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, grid_to_map, submit

parser = argparse.ArgumentParser()
parser.add_argument("--from-std-in", action='store_true', default=False)
args = parser.parse_args()
if args.from_std_in:
    raw_input = clipboard.paste()
else:
    with open("input.txt", "r") as f:
        raw_input = f.read()
if raw_input[-1] == "":
    raw_input = raw_input[:-1]

answer1 = None 
answer2 = None

print("Part 1")
total_1 = 0
invalid_1 = 0
for row in raw_input.split("\n\n"):
    tokens = row.strip().replace("\n", " ").split(" ")
    split_tokens = [t.split(":") for t in tokens]
    to_map = {t[0]: t[1] for t in split_tokens}

    valid = True
    if not set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]).issubset(to_map.keys()):
        valid = False

    if valid:
        total_1 += 1

answer1 = total_1
print(f"Answer: {answer1}")

def validate_range(value, lo, hi):
    if not value.isnumeric() or not lo <= int(value) <= hi:
        return False
    return True

def validate_height(hgt):
    try:
        num = hgt[:-2]
        unit = to_map[att][-2:]
    except:
        return False
    if unit not in ["in", "cm"]:
        return False
    if unit == "cm":
        if not validate_range(num, 150, 193):
            return False
    if unit == "in":
        if not validate_range(num, 59, 76):
            return False
    return True

def validate_hcl(hcl):
    if hcl[0] != "#":
        return False
    if len(hcl) != 7:
        return False
    for c in hcl[1:]:
        if c not in "0123456789abcdef":
            return False
    return True

def validate_pid(pid):
    if len(pid) != 9 or not pid.isnumeric():
        return False
    return True

print("Part 2")
total_2 = 0
for row_num, row in enumerate(raw_input.split("\n\n")):
    tokens = row.strip().replace("\n", " ").split(" ")
    split_tokens = [t.split(":") for t in tokens]
    to_map = {t[0]: t[1] for t in split_tokens}

    valid = True
    if not set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]).issubset(to_map.keys()):
        valid = False
    for att, v in to_map.items():
        if att == "byr":
            if len(v) != 4:
                valid = False
            if not validate_range(v, 1920, 2002):
                valid = False
        elif att == "iyr":
            if len(v) != 4:
                valid = False
            if not validate_range(v, 2010, 2020):
                valid = False
        elif att == "eyr":
            if len(v) != 4:
                valid = False
            if not validate_range(v, 2020, 2030):
                valid = False
        elif att == "hgt":
            if not validate_height(v):
                valid = False
        elif att == "hcl":
            if not validate_hcl(v):
                valid = False
        elif att == "ecl":
            if v not in ["amb", "blu", "brn", "gry", "hzl", "grn", "oth"]:
                valid = False
        elif att == "pid":
            if not validate_pid(v):
                valid = False
        
    if valid:
        total_2 += 1
    
answer2 = total_2

print(f"Answer: {answer2}")