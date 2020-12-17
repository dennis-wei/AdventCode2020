import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, submit, Input, Grid
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

def get_adjacent(i, j, k):
    ret = []
    for di in range(-1, 2):
        for dj in range(-1, 2):
            for dk in range(-1, 2):
                if di == dj == dk == 0:
                    continue
                ret.append((i + di, j + dj, k + dk))
    return ret

class Cube:
    def __init__(self, grid, padding):
        self.base_grid = grid.grid
        self.base_size = grid.height
        self.size = self.base_size + padding * 2
        self.padding = padding
        self.coord_range = range(-padding, self.base_size + self.padding + 1)
        self.reset()
    
    def reset(self):
        self.cube = {}
        for k in self.coord_range:
            for i in self.coord_range:
                for j in self.coord_range:
                    if k == 0:
                        self.cube[(i, j, k)] = self.base_grid.get((i, j), ".")
                    else:
                        self.cube[(i, j, k)] = "."
    
    def iter(self):
        new_cube = {}
        for (i, j, k), v in self.cube.items():
            num_adj_active = sum(self.cube.get(t, ".") == "#" for t in get_adjacent(i, j, k))
            if v == "#" and num_adj_active in [2, 3]:
                new_cube[(i, j, k)] = '#'
            elif v == "." and num_adj_active == 3:
                new_cube[(i, j, k)] = '#'
            else:
                new_cube[(i, j, k)] = '.'
        self.cube = new_cube
    
    def run(self, num_times):
        for i in range(num_times):
            self.iter()
        return sum(v == '#' for v in self.cube.values())

def get_hadjacent(i, j, k, l):
    ret = []
    for dl in range(-1, 2):
        for di in range(-1, 2):
            for dj in range(-1, 2):
                for dk in range(-1, 2):
                    if di == dj == dk == dl == 0:
                        continue
                    ret.append((i + di, j + dj, k + dk, l + dl))
    return ret

class HyperCube:
    def __init__(self, grid, padding):
        self.base_grid = grid.grid
        self.base_size = grid.height
        self.size = self.base_size + padding * 2
        self.padding = padding
        self.coord_range = range(-padding, self.base_size + self.padding + 1)
        self.reset()
    
    def reset(self):
        self.hcube = {}
        for k in self.coord_range:
            for i in self.coord_range:
                for j in self.coord_range:
                    for l in self.coord_range:
                        if k == l == 0:
                            self.hcube[(i, j, k, l)] = self.base_grid.get((i, j), ".")
                        else:
                            self.hcube[(i, j, k, l)] = "."
    
    def iter(self):
        new_hcube = {}
        for (i, j, k, l), v in self.hcube.items():
            num_adj_active = sum(self.hcube.get(t, ".") == "#" for t in get_hadjacent(i, j, k, l))
            if v == "#" and num_adj_active in [2, 3]:
                new_hcube[(i, j, k, l)] = '#'
            elif v == "." and num_adj_active == 3:
                new_hcube[(i, j, k, l)] = '#'
            else:
                new_hcube[(i, j, k, l)] = '.'
        self.hcube = new_hcube
    
    def run(self, num_times):
        for i in range(num_times):
            self.iter()
        return sum(v == '#' for v in self.hcube.values())

def solve(input):
    grid = Grid(input)
    cube = Cube(grid, 6)
    a1 = cube.run(6)

    hcube = HyperCube(grid, 6)
    a2 = hcube.run(6)
    return a1, a2

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(17, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(17, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")