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
        # .ints()
        # .int_tokens()
        # .tokens()
        .lines()
        # .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

class OpNode:
    def __init__(self, op, left, right):
        self.left = left
        self.right = right
        self.op = op
    
    def calc(self):
        if self.op == "+":
            return self.left.calc() + self.right.calc()
        elif self.op == "*":
            return self.left.calc() * self.right.calc()
        elif self.op == "-":
            return self.left.calc() * self.right.calc()
        elif self.op.isnumeric():
            return int(self.op)
    
    def __str__(self):
        if self.op.isnumeric():
            return self.op
        else:
            return f"({self.left} {self.op} {self.right})"
    
    def __repr__(self):
        return self.__str__()

def extract_paren(line, i):
    curr = i
    curr_paren_layer = 1
    acc = ""
    while curr_paren_layer > 0:
        curr += 1
        if line[curr] == "(":
            curr_paren_layer += 1
        elif line[curr] == ")":
            curr_paren_layer -= 1
        acc += line[curr]
    return acc[:-1], curr + 1

def create_tree(line):
    def handle_op(new_node, stack, op_stack):
        if op: 
            left = stack.pop()
            op_node = OpNode(op, left, new_node)
            stack.append(op_node)
        else:
            stack.append(new_node)

    op = None
    stack = deque()
    curr_idx = 0
    while curr_idx < len(line):
        c = line[curr_idx]
        if c == "(":
            clipped_line, curr_idx = extract_paren(line, curr_idx)
            new_node = create_tree(clipped_line)
            handle_op(new_node, stack, op)
            op = None
        elif c.isnumeric():
            new_node = OpNode(c, None, None)
            handle_op(new_node, stack, op)
            op = None
        elif c in "+*-":
            op = c
        curr_idx += 1

    assert(len(stack) == 1)
    return stack[0]

def create_tree_with_oo(line):
    def handle_op(new_node, stack, op_stack):
        if len(op_stack) > 0:
            new_op = op_stack.pop()
            if new_op == "+":
                left = stack.pop()
                op_node = OpNode(new_op, left, new_node)
                stack.append(op_node)
            else:
                stack.append(new_node)
                op_stack.append(new_op)
        else:
            stack.append(new_node)

    op_stack = deque()
    stack = deque()
    curr_idx = 0
    while curr_idx < len(line):
        c = line[curr_idx]
        if c == "(":
            clipped_line, curr_idx = extract_paren(line, curr_idx)
            new_node = create_tree_with_oo(clipped_line)
            handle_op(new_node, stack, op_stack)
        elif c.isnumeric():
            new_node = OpNode(c, None, None)
            handle_op(new_node, stack, op_stack)
        elif c in "+*":
            op_stack.append(c)
        curr_idx += 1

    assert(len(stack) == len(op_stack) + 1)
    while(len(stack) > 1):
        right = stack.pop()
        left = stack.pop()
        op = op_stack.pop()
        stack.append(OpNode(op, left, right))
    
    assert(len(stack) == 1 and len(op_stack) == 0)
    return stack[0]

def solve(input):
    all_res1 = []
    all_res2 = []
    for line in input:
        tree1 = create_tree(line)
        res1 = tree1.calc()
        all_res1.append(res1)

        tree2 = create_tree_with_oo(line)
        res2 = tree2.calc()
        all_res2.append(res2)
    
    return sum(all_res1), sum(all_res2)

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(18, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(18, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")