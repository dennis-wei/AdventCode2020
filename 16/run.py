
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
        # .int_tokens()
        # .tokens()
        # .lines()
        # .line_tokens()
        .line_tokens(sep = "\n", line_sep = "\n\n")
)

def parse_fields(rows):
    by_num = defaultdict(list)
    by_range = defaultdict(list)
    for r in rows:
        field_name = r.split(":")[0]
        l1, h1, l2, h2 = get_all_nums(r)
        by_range[((l1, h1), (l2, h2))] = field_name
        for i in range(l1, h1 + 1):
            by_num[i].append(field_name)
        for i in range(l2, h2 + 1):
            by_num[i].append(field_name)
    return by_num, by_range

def in_range(target_range, elem):
    return target_range[0] <= elem and target_range[1] >= elem

def in_multi_range(target_ranges, input):
    ret = all(in_range(target_ranges[0], e) or in_range(target_ranges[1], e) for e in input)
    return ret

def solve(input):
    by_num, by_range = parse_fields(input[0])
    your_ticket = get_all_nums(input[1][1])
    nearby_tickets = [get_all_nums(r) for  r in input[2][1:]]

    # Part 1
    acc = 0
    valid_tix = []
    for t in nearby_tickets:
        is_valid = True
        for n in t:
            if n not in by_num:
                is_valid = False
                acc += n
        if is_valid:
            valid_tix.append(t)

    # Part 2
    idx_lists = defaultdict(list)
    for t in valid_tix:
        for i, n in enumerate(t):
            idx_lists[i].append(n)

    idx_potentials = defaultdict(set)
    for idx, range in idx_lists.items():
        for target_range, field_names in by_range.items():
            if in_multi_range(target_range, range):
                idx_potentials[idx].add(field_names)
    
    fields = {}
    removed_idx = set()
    while len(idx_potentials) > len(removed_idx):
        singleton = {k: list(v)[0] for k, v in idx_potentials.items() if len(v) == 1 and k not in removed_idx}
        for sk, sv in singleton.items():
            fields[sk] = sv
            for k, v in idx_potentials.items():
                if sv in v:
                    v.remove(sv)
                    if len(v) == 0:
                        removed_idx.add(k)

    print(fields)

    acc2 = 1
    for k, v in fields.items():
        if v.startswith("departure"):
            acc2 *= your_ticket[k]

    return acc, acc2

answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(16, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(16, 2, answer1).text)
