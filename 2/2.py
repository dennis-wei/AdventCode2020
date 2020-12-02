import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from itertools import combinations
from collections import defaultdict
from util.helpers import space_split_input

input = space_split_input()

print("Part 1")
total = 0
for i in input:
    rng, char_token, password = i
    low, high = [int(t) for t in rng.split("-")]
    char = char_token[0]
    n = 0
    for p in password:
        if p == char:
            n += 1
    if low <= n and high >= n:
        total += 1
print(f"Answer to part 1: {total}")

print("Part 2")
total2 = 0
for i in input:
    rng, char_token, password = i
    low, high = [int(t) for t in rng.split("-")]
    char = char_token[0]
    clow = password[low - 1] == char
    chigh = password[high - 1] == char
    if clow ^ chigh:
        total2 += 1
print(f"Answer to part 2: {total2}")