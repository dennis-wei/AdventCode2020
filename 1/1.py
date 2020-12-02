import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from itertools import combinations
from util.helpers import int_parsed_input

input = int_parsed_input()

print("Part 1")
for i in input:
    if 2020 - i in input:
        n2 = 2020 - i
        print(f"n1: {i}, n2: {n2}. Answer: {i * n2}")
        break

print("Part 2")
for i, j in combinations(input, 2):
    if 2020 - (i + j) in input:
        n3 = 2020 - (i + j)
        print(f"n1: {i}, n2: {j} n3: {n3}. Answer: {i * j * n3}")
        break
