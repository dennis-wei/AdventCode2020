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

def parse_potential_ingredients(row, potential_allergen_ingredients, all_ingredients, ingredient_counts):
    ingredients_str, allergens_str = row.split(" (contains ")
    ingredients = ingredients_str.split(" ")
    allergens = allergens_str[:-1].split(", ")

    for allergen in allergens:
        if not allergen in potential_allergen_ingredients:
            potential_allergen_ingredients[allergen] = set(ingredients)
        else:
            potential_allergen_ingredients[allergen] = potential_allergen_ingredients[allergen] & set(ingredients)
    
    for ingredient in ingredients:
        ingredient_counts[ingredient] += 1
    
    all_ingredients.update(ingredients)




def solve(input):
    potential_allergen_ingredients = {}
    all_ingredients = set()
    ingredient_counts = defaultdict(int)
    for row in input:
        parse_potential_ingredients(row, potential_allergen_ingredients, all_ingredients, ingredient_counts)
    
    potential_allergens = set()
    for v in potential_allergen_ingredients.values():
        potential_allergens.update(v)
    
    safe_ingredients = all_ingredients - potential_allergens

    handled_ingredients = set()
    mapping = {}
    while len(handled_ingredients) < len(potential_allergens):
        singletons = {k: v for k, v in potential_allergen_ingredients.items() if len(v) == 1}
        for all, ing_set in singletons.items():
            ing = list(ing_set)[0]
            for other_ing_set in potential_allergen_ingredients.values():
                if ing in other_ing_set:
                    other_ing_set.remove(ing)
            handled_ingredients.add(ing)
            mapping[ing] = all

    print("ingredient mapping: ", mapping)

    return sum(v for k, v in ingredient_counts.items() if k in safe_ingredients), ','.join(sorted(list(handled_ingredients), key = lambda x: mapping[x]))


start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(21, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(21, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")