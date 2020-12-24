import time
import os, sys

from requests.api import get
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import get_all_nums, submit, Input, Grid
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

    
def parse(dir):
    idx = 0
    acc = ""
    ret = []
    while idx < len(dir):
        if dir[idx] in "ns":
            acc += dir[idx]
        else:
            ret.append(acc + dir[idx])
            acc = ""
        idx += 1
    return ret

def get_idx(dirs):
    curr_idx = (0, 0)
    for d in dirs:
        x, y = curr_idx
        if d == "w":
            curr_idx = (x - 2, y)
        elif d == "e":
            curr_idx = (x + 2, y)
        elif d == "se":
            curr_idx = (x + 1, y + 1)
        elif d == "sw":
            curr_idx = (x - 1, y + 1)
        elif d == "ne":
            curr_idx = (x + 1, y - 1)
        elif d == "nw":
            curr_idx = (x - 1, y - 1)
        else:
            print("Unhandled direction: ", d)
            sys.exit(1)
    return curr_idx

def get_neighbors(x, y):
    return [
        (x - 2, y),
        (x + 2, y),
        (x - 1, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y + 1)
    ]

class HexagonGrid:
    def __init__(self):
        self.grid = defaultdict(lambda: 0)
    
    def init_row(self, row):
        dirs = parse(row)
        idx = get_idx(dirs)
        self.grid[idx] = int(not self.grid[idx])
    
    def get_num_black(self):
        return sum(1 for v in self.grid.values() if v == 1)
    
    def grid_fill(self):
        xmin = min(t[0] for t in self.grid)
        xmax = max(t[0] for t in self.grid)
        ymin = min(t[1] for t in self.grid)
        ymax = max(t[1] for t in self.grid)

        for x in range(xmin - 85, xmax + 85):
            for y in range(ymin - 55, ymax + 55):
                if (x, y) not in self.grid:
                    self.grid[(x, y)] = 0
    
    def iter(self):
        new_grid = defaultdict(lambda: 0)
        for tile, color in self.grid.items():
            neighbors = get_neighbors(*tile)
            nnbt = sum(self.grid.get(n, 0) for n in neighbors)
            if color == 1 and (nnbt == 0 or nnbt > 2):
                new_grid[tile] = 0
            elif color == 0 and nnbt == 2:
                new_grid[tile] = 1
            else:
                new_grid[tile] = color
        
        self.grid = new_grid


def solve(input):
    hex = HexagonGrid()
    for row in input:
        hex.init_row(row)
    
    a1 = hex.get_num_black()

    hex.grid_fill()
    for i in range(100):
        hex.iter()
        if i % 10 == 9:
            print(f"Day {i + 1}: ", hex.get_num_black())
    print()

    a2 = hex.get_num_black()

    return a1, a2

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(24, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(24, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")