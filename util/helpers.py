def parse_input():
    with open(f"input.txt", "r") as f:
        input = [l.strip() for l in f]
    return input

def space_split_input():
    with open(f"input.txt", "r") as f:
        input = [l.strip().split(" ") for l in f]
    return input

def int_parsed_input():
    with open(f"input.txt", "r") as f:
        input = [int(l) for l in f]
    return input