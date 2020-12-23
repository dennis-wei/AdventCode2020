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

class FastCircle:
    def __init__(self, orig_list):
        self.next_mapping = {}
        for i in range(len(orig_list) - 1):
            self.next_mapping[orig_list[i]] = orig_list[i + 1]
        self.next_mapping[orig_list[-1]] = orig_list[0]

        self.curr_cup = orig_list[0]
        self.max_cup = max(orig_list)
    
    def __repr__(self):
        orig_cup = self.curr_cup
        acc = ''
        for i in range(self.max_cup):
            acc += str(self.curr_cup)
            self.curr_cup = self.next_mapping[self.curr_cup]
        self.curr_cup = orig_cup
        return acc
    
    def __str__(self):
        return self.__repr__()
    
    def iter(self):
        removed = self.next_mapping[self.curr_cup]
        removed_next = self.next_mapping[removed]
        removed_next_next = self.next_mapping[self.next_mapping[removed]]

        self.next_mapping[self.curr_cup] = self.next_mapping[removed_next_next]

        not_valid = set()
        not_valid.add(removed)
        not_valid.add(removed_next)
        not_valid.add(removed_next_next)

        v = self.curr_cup - 1
        if v == 0:
            v = self.max_cup
        while v in not_valid:
            v = v - 1
            if v == 0:
                v = self.max_cup
        
        temp = self.next_mapping.pop(v)
        self.next_mapping[v] = removed
        self.next_mapping[removed_next_next] = temp

        self.curr_cup = self.next_mapping[self.curr_cup]

    def run(self, n):
        for i in range(n):
            self.iter()
        
        next = self.next_mapping[1]
        acc = []
        while True:
            if next == 1:
                break
            acc.append(next)
            next = self.next_mapping[next]
        
        return ''.join(str(n) for n in acc)
    
    def run2(self, n):
        for i in range(n):
            self.iter()
        
        next = self.next_mapping[1]
        next_next = self.next_mapping[next]
        return next * next_next

def solve(input):
    modified_input1 = [int(n) for n in str(input[0])]
    runner = FastCircle(modified_input1)
    a1 = runner.run(100)

    modified_input2 = [int(n) for n in str(input[0])]
    start = max(modified_input2)
    for i in range(start + 1, 1000001):
        modified_input2.append(i)
    runner2 = FastCircle(modified_input2)
    a2 = runner2.run2(10000000)
    return a1, a2 

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(23, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(23, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")