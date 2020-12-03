import os
import re
import requests

def split_newline(i):
    return [l for l in i.split("\n")]

def space_split(input):
    return [l.split(" ") for l in input]

def int_parsed_list(input):
    return [int(l) for l in input]

def list_of_ints(l):
    return [int(e) for e in l]

def get_all_nums(s):
    return list_of_ints(re.findall(r'\d+', s))

def grid_to_map(i, index_by_one=False, split_input=False):
    if split_input:
        i = i.split("\n")
    result = {}
    for row_number, row in enumerate(i):
        for col_number, char in enumerate(row.strip()):
            if index_by_one:
                k = (row_number + 1, col_number + 1)
            else:
                k = (row_number, col_number)
            result[k] = char
    return result
            

def submit(day, part, answer):
    print(os.environ['ADVENT_SESSION'])
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f"session={os.environ['ADVENT_SESSION']}",
        'DNT': "1"
    }
    return requests.post(f"https://adventofcode.com/2020/day/{day}/answer", data = f"level={part}&answer={answer}", headers=headers)
    