
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


dir_mapping = {
    0: "E",
    90: "N",
    180: "W",
    270: "S"
}

update_map = {
    "N": (0, 1),
    "S": (0, -1),
    "E": (1, 0),
    "W": (-1, 0)
}

def move(coord, dir, factor):
    update = update_map[dir]
    return (coord[0] + factor * update[0], coord[1] + factor * update[1])

def turn(dir, num, curr_angle):
    if dir == "L":
        return (curr_angle + num) % 360
    elif dir == "R":
        return (curr_angle - num) % 360
        
def rotate_waypoint_right(num, curr_waypoint):
    for i in range(num // 90):
        curr_waypoint = (curr_waypoint[1], -curr_waypoint[0])
    return curr_waypoint

def rotate_waypoint(dir, num, curr_waypoint):
    if dir == "R":
        return rotate_waypoint_right(num, curr_waypoint)
    else:
        return rotate_waypoint_right(360 - num, curr_waypoint)

def move_to_waypoint(curr_coord, curr_waypoint, factor):
    return (curr_coord[0] + factor * curr_waypoint[0], curr_coord[1]  + factor * curr_waypoint[1])

assert(move((0, 0), "N", 10) == (0, 10))
assert(move((0, 0), "E", 10) == (10, 0))
assert(move((0, 0), "S", 10) == (0, -10))
assert(move((0, 0), "W", 10) == (-10, 0))

assert(turn("L", 90, 0) == 90)
assert(turn("R", 90, 0) == 270)

def solve1(input):
    curr_coord = (0, 0)
    curr_angle = 0

    for r in input:
        dir = r[0]
        num = int(r[1:])
        if dir in "NSEW":
            curr_coord = move(curr_coord, dir, num)
        elif dir in "LR":
            curr_angle = turn(dir, num, curr_angle)
        elif dir == "F":
            curr_coord = move(curr_coord, dir_mapping[curr_angle], num)
    
    return sum(abs(n) for n in curr_coord)

def solve2(input):
    curr_coord = (0, 0)
    curr_waypoint = (10, 1)
    for r in input:
        dir = r[0]
        num = int(r[1:])

        if dir in "NSEW":
            curr_waypoint = move(curr_waypoint, dir, num)
        elif dir in "LR":
            curr_waypoint = rotate_waypoint(dir, num, curr_waypoint)
        elif dir == "F":
            curr_coord = move_to_waypoint(curr_coord, curr_waypoint, num)

    return sum(abs(n) for n in curr_coord)

answer1, answer2 = (solve1(input), solve2(input))

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(12, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(12, 2, answer1).text)
