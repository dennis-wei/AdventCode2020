
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations, count
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
if raw_input[-1] == "":
    raw_input = raw_input[:-1]

input = raw_input

def solve(input):
    mapping = defaultdict(list)
    inv_mapping = defaultdict(list)
    inv_mapping_count = defaultdict(dict)
    base_bags = set()
    for row in input.split("\n"):
        if row == "":
            break
        left, right = row.split(" contain ")
        left_color = " ".join(left.split(" ")[:2])
        inner_bags = []
        for inner_bag in right.split(", "):
            if "no" in inner_bag:
                mapping[left_color] = []
                base_bags.add(left_color)
                break
            n = get_all_nums(inner_bag)[0]
            color = " ".join(inner_bag.split(" ")[-3:-1]).replace(".", "")
            inner_bags.append((color, n))
            inv_mapping[color].append(left_color)
        mapping[left_color] = inner_bags
        
    encountered = set()
    queue = list()
    queue.append("shiny gold")
    while len(queue) > 0:
        color = queue.pop()
        encountered.add(color)
        for new_color in inv_mapping[color]:
            if new_color not in encountered:
                queue.append(new_color)

    count_memo = {b: 1 for b in base_bags}
    def recurse(bag):
        if bag in count_memo:
            return count_memo[bag]
        s = 1
        for inner_bag, num_bags in mapping[bag]:
            s += num_bags * recurse(inner_bag)
        count_memo[bag] = s
        return s

    return len(encountered) - 1, recurse("shiny gold") - 1

answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(7, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(7, 2, answer1).text)
