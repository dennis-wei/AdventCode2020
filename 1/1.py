from itertools import combinations

with open("input.txt", "r") as f:
    input = set(int(l.strip()) for l in f)

print("Part 1")
for i in input:
    if 2020 - i in input:
        n2 = 2020 - i
        print(f"n1: {i}, n2: {n2}. Answer: {i * n2}")
        break

for i, j in combinations(input, 2):
    if 2020 - (i + j) in input:
        n3 = 2020 - (i + j)
        print(f"n1: {i}, n2: {j} n3: {n3}. Answer: {i * j * n3}")
        break
