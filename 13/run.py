
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, submit, Input
from math import floor, ceil, gcd
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

def solve(input):
    def solve1(input):
        et = int(input[0])
        ids = get_all_nums(input[1])
        multipliers = defaultdict(int)
        multipliers = {k: ceil(et / k) * k for k in ids}
        inv_multipliers = {v: k for k, v in multipliers.items()}
        m = min(multipliers.values())
        return (m - et) * inv_multipliers[m]

    def lcm(n1, n2):
        return abs(n1 * n2) // gcd(n1, n2)

    def solve2_pair(e1, e2):
        bus1_offset, bus1_mod = max((e1, e2), key = lambda x: x[1])
        bus2_offset, bus2_mod = min((e1, e2), key = lambda x: x[1])
        acc = 0
        while True:
            acc += bus1_mod
            if (acc + bus1_offset) % bus2_mod == bus2_offset % bus2_mod:
                break
        return acc + bus1_offset, lcm(bus1_mod, bus2_mod)
    
    def solve2(input):
        bus_ids = input.split(",")
        offset_bus_ids = deque()
        for i, id in enumerate(bus_ids):
            if id.isnumeric():
                offset_bus_ids.append((int(id) - i, int(id)))
        
        while len(offset_bus_ids) > 1:
            first_pair = offset_bus_ids.popleft()
            second_pair = offset_bus_ids.popleft()
            offset_bus_ids.appendleft(solve2_pair(first_pair, second_pair))
        
        result = offset_bus_ids.popleft()
        return result[0]

    assert(solve2("17,x,13,19")) == 3417
    assert(solve2("67,7,59,61")) == 754018
    assert(solve2("67,x,7,59,61")) == 779210
    assert(solve2("67,7,x,59,61")) == 1261476
    assert(solve2("1789,37,47,1889")) == 1202161486

    return solve1(input), solve2(input[1])
    
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(13, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(13, 2, answer1).text)
