
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

class Seats:
    def __init__(self, input):
        self.grid = {}
        self.height = len(input)
        self.length = len(input[0])
        for row_num, row in enumerate(input):
            for col_num, c in enumerate(row):
                self.grid[(row_num, col_num)] = c
        
        self.grid2 = deepcopy(self.grid)
    
    def get_adjacent(self, grid, x, y):
        ret = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j and i == 0:
                    continue
                if (x + i, y + j) in grid:
                    ret.append(grid[x + i, y + j])
        return ret
    
    def print_grid(self, grid):
        for i in range(self.height):
            for j in range(self.length):
                print(grid[i, j], end="")
            print()
        print()
    
    def iterate(self):
        new_grid = {}
        for coord, initial in self.grid.items():
            if initial == "L":
                if all(a == "L" or a  == "." for a in self.get_adjacent(self.grid, *coord)):
                    new_grid[coord] = "#"
                    continue
            if initial == "#":
                if sum(a == "#" for a in self.get_adjacent(self.grid, *coord)) >= 4:
                    new_grid[coord] = "L"
                    continue
            new_grid[coord] = initial

        if self.grid == new_grid:
            return True

        self.grid = new_grid
        return False
    
    def get_visible(self, grid, x, y):
        num_visible = 0
        for (xd, yd) in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            multiplier = 1
            while True:
                coord_to_check = (x + xd * multiplier, y + yd * multiplier)
                if coord_to_check not in grid:
                    break
                if grid[coord_to_check] == "#":
                    num_visible += 1
                    break
                if grid[coord_to_check] == "L":
                    break
                multiplier += 1
        return num_visible

    
    def iterate2(self):
        new_grid = {}
        for coord, initial in self.grid2.items():
            if initial == "L":
                if self.get_visible(self.grid2, *coord) == 0:
                    new_grid[coord] = "#"
                    continue
            if initial == "#":
                if self.get_visible(self.grid2, *coord) >= 5:
                    new_grid[coord] = "L"
                    continue
            new_grid[coord] = initial

        if self.grid2 == new_grid:
            return True

        self.grid2 = new_grid
        return False

    def run(self):
        while True:
            if self.iterate():
                break
        
        while True:
            if self.iterate2():
                break
        
        return sum(v == "#" for v in self.grid.values()), sum(v == "#" for v in self.grid2.values())


def solve(input):
    seats = Seats(input)
    answer1, answer2 = seats.run()
    
    return seats.run()

answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(11, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(11, 2, answer1).text)
