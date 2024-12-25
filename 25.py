# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import Counter, defaultdict, deque
from functools import cache
from math import floor

input_value = open("25.txt", "r").read()
locks_and_keys = input_value.split("\n\n")


def add_same_type_length_tuples(first, second):
    return tuple(first[i] + second[i] for i in range(len(first)))


locks = []
keys = []

for item in locks_and_keys:
    item = item.split("\n")
    is_lock = item[0][0] == "#"
    row_range = range(len(item)) if is_lock else range(len(item) - 1, -1, -1)
    heights = []
    for c in range(len(item[0])):
        height = 0
        for r in row_range:
            if item[r][c] != "#":
                break
            height += 1
        heights.append(height)
    if is_lock:
        locks.append(heights)
    else:
        keys.append(heights)

# Part 1:
count_combos = 0
max_target = 7
for lock in locks:
    for key in keys:
        if all(
            height <= max_target for height in add_same_type_length_tuples(lock, key)
        ):
            count_combos += 1
print(count_combos)
