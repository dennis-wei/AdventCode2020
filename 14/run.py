
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
        # .ints()
        # .tokens()
        .lines()
        # .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

def get_mask(row):
    mask = row.split(" = ")[-1]
    mask_map = {}
    for idx, b in enumerate(mask[::-1]):
        if b.isnumeric():
            mask_map[idx] = b
    max_idx = max(mask_map.keys()) + 1
    return {k: v for k, v in mask_map.items() if k <= max_idx}, max_idx

def solve1(input):
    mem_slots = defaultdict(int)
    max_idx = 0
    mask_map = {}

    def apply_mask(bin_str, mask_map):
        acc = ""
        for idx, b in enumerate(bin_str[::-1]):
            if idx in mask_map:
                acc += mask_map[idx]
            else:
                acc += b
        in_bin = acc[::-1]
        return int(in_bin, 2)

    for row in input:
        if row.startswith("mask"):
            mask_map, max_idx = get_mask(row)
            continue

        target_mem, base_num = get_all_nums(row)
        bin_str = "{0:b}".format(base_num)
        if len(bin_str) < max_idx:
            bin_str = "0" * (max_idx - len(bin_str)) + bin_str

        mem_slots[target_mem] = apply_mask(bin_str, mask_map)

    return sum(v for v in mem_slots.values())

def get_fluc_mask(row):
    mask = row.split(" = ")[-1]
    mask_map = {}
    for idx, b in enumerate(mask[::-1]):
        mask_map[idx] = b
    max_idx = max(k for k, v in mask_map.items() if v != "0") + 1
    return {k: v for k, v in mask_map.items() if k <= max_idx}, max_idx

def solve2(input):
    mem_slots = defaultdict(int)
    max_idx = 0
    mask_map = {}

    def get_poss_bin_str(fluc_bin_str, acc):
        if len(fluc_bin_str) == 0:
            return acc
        char_to_add = fluc_bin_str[0]
        if char_to_add in "01":
            new_acc = [acc_elem + char_to_add for acc_elem in acc]
            return get_poss_bin_str(fluc_bin_str[1:], new_acc)
        else:
            with_ones = [acc_elem + "1" for acc_elem in acc]
            with_zeroes = [acc_elem + "0" for acc_elem in acc]
            return get_poss_bin_str(fluc_bin_str[1:], with_ones + with_zeroes)
    
    def get_mem_addrs(bin_str, mask_map, max_idx):
        acc = ""
        # print(bin_str, mask_map)
        for idx, b in enumerate(bin_str[::-1]):
            if idx in mask_map and mask_map[idx] in "1X":
                acc += mask_map[idx]
            else:
                acc += b

        fluc_bin_str = acc[::-1]
        # print(fluc_bin_str)
        return[int(s, 2) for s in get_poss_bin_str(fluc_bin_str, [""])]

    for row in input:
        if row.startswith("mask"):
            mask_map, max_idx = get_fluc_mask(row)
            continue
        
        target_mem, base_num = get_all_nums(row)
        bin_str = "{0:b}".format(target_mem)
        if len(bin_str) < max_idx:
            bin_str = "0" * (max_idx - len(bin_str)) + bin_str

        mem_addrs = get_mem_addrs(bin_str, mask_map, max_idx)
        for m in mem_addrs:
            mem_slots[m] = base_num
    return sum(v for v in mem_slots.values())
        

answer1, answer2 = solve1(input), solve2(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(14, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(14, 2, answer1).text)
