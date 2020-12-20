import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, submit, Input, Grid
from math import floor, ceil, sqrt
from functools import reduce
from copy import deepcopy

from colorama import Fore, Style

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
        # .lines()
        # .line_tokens()
        .line_tokens(sep = "\n", line_sep = "\n\n")
)

GRID_SIZE = 10

def print_grid(grid):
    for row in grid:
        for char in row:
            print(char, end="")
        print()

def rotate_grid_clockwise(grid):
    rotated_grid = deepcopy(grid)
    for i in range (0, len(grid)):
        for j in range (0, len(grid)):
            rotated_grid[i][j] = grid[-(j+1)][i][:]
    return rotated_grid

def rotate_grid_counterclockwise(grid):
    rotated_grid = deepcopy(grid)
    for i in range(3):
        rotated_grid = rotate_grid_clockwise(grid)
    return rotated_grid

def flip_vertically(grid):
    return grid[::-1]

def flip_horizontally(grid):
    return [r[::-1] for r in grid]

class Tile:
    def get_axis(self, y, x):
        acc = []
        if y == 0:
            acc = [self.grid[i][0] for i in range(GRID_SIZE)]
        elif y == 1:
            acc = [self.grid[i][GRID_SIZE - 1] for i in range(GRID_SIZE)]
        elif x == 0:
            acc = [self.grid[0][i] for i in range(GRID_SIZE)]
        elif x == 1:
            acc = [self.grid[GRID_SIZE - 1][i] for i in range(GRID_SIZE)]
        return tuple(acc)
    
    def rotate_clockwise(self):
        # print("rot")
        self.grid = rotate_grid_clockwise(self.grid)

        self.left = self.get_axis(0, None)
        self.right = self.get_axis(1, None)
        self.up = self.get_axis(None, 0)
        self.down = self.get_axis(None, 1)

    def flip(self):
        # print("flip")
        self.grid = flip_vertically(self.grid)

        self.left = self.get_axis(0, None)
        self.right = self.get_axis(1, None)
        self.up = self.get_axis(None, 0)
        self.down = self.get_axis(None, 1)
    
    def iter_orientation(self):
        if not self.initial_iter:
            self.initial_iter = True
            return False

        if self.times_rotated < 4:
            self.rotate_clockwise()
            self.times_rotated += 1
            return False
        
        if self.flipped:
            print(f"went through all iterations of tile {self.id}")
            return True
        
        self.times_rotated = 0
        self.flip()
        self.flipped = True
        return False
    
    def stripped(self):
        return [r[1:-1] for r in self.grid[1:-1]]

    def __init__(self, id, grid_list):
        self.id = id
        self.grid = [list(r) for r in grid_list]
        self.left = self.get_axis(0, None)
        self.right = self.get_axis(1, None)
        self.up = self.get_axis(None, 0)
        self.down = self.get_axis(None, 1)

        self.initial_iter = False
        self.times_rotated = 0
        self.flipped = 0

        self.edge_map = {
            "up": self.up,
            "down": self.down,
            "left": self.left,
            "right": self.right
        }
    
    def __str__(self):
        acc = "\n"
        for row in self.grid:
            for char in row:
                acc += char
            acc += "\n"
        return acc
    
    def __repr__(self):
        return self.__str__()

def get_matches(tiles):
    by_pattern = defaultdict(list)
    for id, tile in tiles.items():
        by_pattern[tile.up].append((id, "up"))
        by_pattern[tile.up[::-1]].append((id, "up_reverse"))

        by_pattern[tile.down].append((id, "down"))
        by_pattern[tile.down[::-1]].append((id, "down_reverse"))

        by_pattern[tile.left].append((id, "up"))
        by_pattern[tile.left[::-1]].append((id, "left_reverse"))

        by_pattern[tile.right].append((id, "up"))
        by_pattern[tile.right[::-1]].append((id, "right"))

    by_id = defaultdict(lambda: defaultdict(list))
    for id, tile in tiles.items():
        by_id[id]["up"] = [p for p in by_pattern[tile.up] if p[0] != id]
        by_id[id]["up_reverse"] = [p for p in by_pattern[tile.up[::-1]] if p[0] != id]

        by_id[id]["down"] = [p for p in by_pattern[tile.down] if p[0] != id]
        by_id[id]["down_reverse"] = [p for p in by_pattern[tile.down[::-1]] if p[0] != id]

        by_id[id]["left"] = [p for p in by_pattern[tile.left] if p[0] != id]
        by_id[id]["left_reverse"] = [p for p in by_pattern[tile.left[::-1]] if p[0] != id]

        by_id[id]["right"] = [p for p in by_pattern[tile.right] if p[0] != id]
        by_id[id]["right_reverse"] = [p for p in by_pattern[tile.right[::-1]] if p[0] != id]
    
    return by_pattern, by_id

def construct_top_row(tiles, by_pattern, puzzle):
    puzzle_size = int(sqrt(len(tiles)))
    curr_tile = puzzle[0][0]
    for i in range(puzzle_size - 2):
        # print(f"Finding match for tile {curr_tile.id} with right {''.join(curr_tile.right)}")
        new_tile = None
        found = False
        for potential_new_tile in by_pattern[curr_tile.right]:
            new_tile = tiles[potential_new_tile[0]]
            if new_tile.id == curr_tile.id:
                continue
            # print(f"Testing tile {potential_new_tile[0]}")
            works = False
            while True:
                done_with_iterations = new_tile.iter_orientation()
                if done_with_iterations:
                    print(f"done with iterations for tile {new_tile.id}")
                    break

                if (new_tile.left == curr_tile.right and len(by_pattern[new_tile.up]) == 1):
                    works = True
                    break
            if works == True:
                found = True
                break
            
        if found:
            puzzle[0][i + 1] = new_tile
            curr_tile = new_tile
        else:
            print(f"Error: found no matching tile while handling tile {curr_tile.id}")
            sys.exit(1)
    
    found = False
    for potential_top_right in by_pattern[curr_tile.right]:
        new_tile = tiles[potential_top_right[0]]
        if new_tile.id == curr_tile.id:
            continue
        # print(f"Testing tile {potential_top_right[0]}")
        works = False
        while True:
            done_with_iterations = new_tile.iter_orientation()
            if done_with_iterations:
                print(f"done with iterations for tile {new_tile.id}")
                break

            if (new_tile.left == curr_tile.right and len(by_pattern[new_tile.up]) == 1 and len(by_pattern[new_tile.right]) == 1):
                works = True
                break
        if works == True:
            found = True
            break
    if found:
        puzzle[0][-1] = new_tile
    else:
        print(f"Error: found no matching tile while handling tile {curr_tile.id}")
        sys.exit(1)

def construct_inner_row(tiles, by_pattern, puzzle, row_num):
    puzzle_size = int(sqrt(len(tiles)))
    seed_tile = puzzle[row_num - 1][0]
    # print(f"Finding match for seed tile {seed_tile.id} with down {''.join(seed_tile.down)}")
    new_tile = None
    found = False
    for potential_new_tile in by_pattern[seed_tile.down]:
        new_tile = tiles[potential_new_tile[0]]
        if new_tile.id == seed_tile.id:
            continue
        # print(f"Testing tile {potential_new_tile[0]}")
        works = False
        while True:
            done_with_iterations = new_tile.iter_orientation()
            if done_with_iterations:
                print(f"done with iterations for tile {new_tile.id}")
                break

            if (new_tile.up == seed_tile.down and len(by_pattern[new_tile.left]) == 1):
                works = True
                break
        if works == True:
            found = True
            break
        
    if found:
        puzzle[row_num][0] = new_tile
        curr_tile = new_tile
    else:
        print(f"Error: found no matching tile while handling tile {seed_tile.id}")
        sys.exit(1)
    
    for i in range(puzzle_size - 2):
        # print(f"Finding match for tile {curr_tile.id} with right {''.join(curr_tile.right)}")
        new_tile = None
        found = False
        for potential_new_tile in by_pattern[curr_tile.right]:
            new_tile = tiles[potential_new_tile[0]]
            if new_tile.id == curr_tile.id:
                continue
            # print(f"Testing tile {potential_new_tile[0]}")
            works = False
            while True:
                done_with_iterations = new_tile.iter_orientation()
                if done_with_iterations:
                    # print(f"done with iterations for tile {new_tile.id}")
                    break

                if (new_tile.left == curr_tile.right and new_tile.up == puzzle[row_num - 1][i + 1].down):
                    works = True
                    break
            if works == True:
                found = True
                break
            
        if found:
            puzzle[row_num][i + 1] = new_tile
            curr_tile = new_tile
        else:
            print(f"Error: found no matching tile while handling tile {curr_tile.id}")
            sys.exit(1)
    
    found = False
    for potential_right in by_pattern[curr_tile.right]:
        new_tile = tiles[potential_right[0]]
        if new_tile.id == curr_tile.id:
            continue
        # print(f"Testing tile {potential_right[0]}")
        works = False
        while True:
            done_with_iterations = new_tile.iter_orientation()
            if done_with_iterations:
                print(f"done with iterations for tile {new_tile.id}")
                break

            if (new_tile.left == curr_tile.right and puzzle[row_num - 1][-1].down == new_tile.up):
                works = True
                break
        if works == True:
            found = True
            break
    if found:
        puzzle[row_num][-1] = new_tile
    else:
        print(f"Error: found no matching tile while handling tile {curr_tile.id}")
        sys.exit(1)


def build_puzzle(tiles, corners, by_pattern):
    puzzle_size = int(sqrt(len(tiles)))
    puzzle = [[None for i in range(puzzle_size)] for j in range(puzzle_size)]
    top_left = tiles[corners[0]]
    top_left.flip()
    while not (len(by_pattern[top_left.up]) == 1 and len(by_pattern[top_left.left]) == 1):
        top_left.iter_orientation()
    puzzle[0][0] = top_left

    construct_top_row(tiles, by_pattern, puzzle)
    for i in range(puzzle_size - 1):
        construct_inner_row(tiles, by_pattern, puzzle, i + 1)

    print("final puzzle")
    for row in puzzle:
        print(', '.join(str(t.id) for t in row))
    print()


    return puzzle
    

def get_corners(by_id):
    dirs = ["up", "down", "left", "right"]

    corners = []
    for id, mapping in by_id.items():
        if len([dir for dir in dirs if len(mapping[dir]) > 0]) == 2:
            corners.append(id)
        
    return corners

def combine_puzzle(puzzle):
    acc = []
    for row_num in range((GRID_SIZE - 2) * len(puzzle)):
        row = []
        corresponding_puzzle_row = row_num // (GRID_SIZE - 2)
        corresponding_inner_row = row_num % (GRID_SIZE - 2)
        for puzzle_tile in puzzle[corresponding_puzzle_row]:
            row.extend(puzzle_tile.stripped()[corresponding_inner_row])
        acc.append(row)

    tile = Tile(0, acc)
    return tile

def get_num_dragons(grid):
    as_dict = {}
    for row_num, row in enumerate(grid):
        for col_num, char in enumerate(row):
            as_dict[(row_num, col_num)] = char
    
    num_dragons = 0
    for sx, sy in as_dict:
        if as_dict.get((sx, sy), 'l') == '#' and \
            as_dict.get((sx - 1, sy + 18), ';') in '#O' and \
            as_dict.get((sx + 1, sy + 1), ';') in '#O' and \
            as_dict.get((sx + 1, sy + 4), ';') in '#O' and \
            as_dict.get((sx + 0, sy + 5), ';') in '#O' and \
            as_dict.get((sx + 0, sy + 6), ';') in '#O' and \
            as_dict.get((sx + 1, sy + 7), ';') in '#O' and \
            as_dict.get((sx + 1, sy + 10), ';') in '#O' and \
            as_dict.get((sx + 0, sy + 11), ';') in '#O' and \
            as_dict.get((sx + 0, sy + 12), ';') in '#O' and \
            as_dict.get((sx + 1, sy + 13), ';') in '#O' and \
            as_dict.get((sx + 1, sy + 16), ';') in '#O' and \
            as_dict.get((sx + 0, sy + 17), ';') in '#O' and \
            as_dict.get((sx + 0, sy + 18), ';') in '#O' and \
            as_dict.get((sx + 0, sy + 19), ';') in '#O':
            num_dragons += 1
            for coord in [
                (sx, sy),
                (sx - 1, sy + 18),
                (sx + 1, sy + 1),
                (sx + 1, sy + 4),
                (sx + 0, sy + 5),
                (sx + 0, sy + 6),
                (sx + 1, sy + 7),
                (sx + 1, sy + 10),
                (sx + 0, sy + 11),
                (sx + 0, sy + 12),
                (sx + 1, sy + 13),
                (sx + 1, sy + 16),
                (sx + 0, sy + 17),
                (sx + 0, sy + 18),
                (sx + 0, sy + 19)
            ]:
                as_dict[coord] = 'O'


    if num_dragons > 0:
        print()
        print("Correctly orientated puzzle")
        for i in range(len(grid)):
            for j in range(len(grid)):
                char = as_dict[(i, j)]
                if char == '.':
                    print(f"{Fore.BLUE}.{Style.RESET_ALL}", end = "")
                elif char == '#':
                    print(f"{Fore.BLUE}^{Style.RESET_ALL}", end = "")
                elif char == 'O':
                    print(f"{Fore.GREEN}O{Style.RESET_ALL}", end = "")
            print()
    return num_dragons, sum(v == '#' for v in as_dict.values())


def solve(input):
    tiles = {}
    for tile in input:
        id, grid_list = int(get_all_nums(tile[0])[0]), tile[1:]
        new_tile = Tile(id, grid_list)
        tiles[id] = new_tile

    by_pattern, by_id = get_matches(tiles)
    corners = get_corners(by_id)

    puzzle = build_puzzle(tiles, corners, by_pattern)
    combined_puzzle = combine_puzzle(puzzle)

    exhausted_options = False
    while not exhausted_options:
        exhausted_options = combined_puzzle.iter_orientation()
        num_dragons, num_pounds = get_num_dragons(combined_puzzle.grid)
        if num_dragons > 0:
            a2 = num_pounds
            break

    return reduce(lambda x, y: x * y, corners, 1), a2 

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(20, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(20, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")