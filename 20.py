# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

import sys
from collections import defaultdict, deque

sys.setrecursionlimit(10000)
input_value = open("20.txt", "r").read()
lines = input_value.split("\n")
rows = len(lines)
columns = len(lines[0])

start, end = None, None
grid = defaultdict(lambda: None)
for r in range(rows):
    for c in range(columns):
        grid[r, c] = lines[r][c]
        if grid[r, c] == "S":
            start = (r, c)
        elif grid[r, c] == "E":
            end = (r, c)


def explore_to_end(
    steps_from_start, cheat_savings, cheat_savings_minimum, position, current_steps
):
    (r, c) = position
    if grid[r, c] in "S.E":
        steps_from_start[r, c] = current_steps
        if grid[r, c] == "E":
            return
        # Force `steps_from_start` to populate first via DFS.
        for neighbor in {(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)}:
            if grid[neighbor] is None:
                continue
            if grid[neighbor] in ".E" and neighbor not in steps_from_start:
                explore_to_end(
                    steps_from_start,
                    cheat_savings,
                    cheat_savings_minimum,
                    neighbor,
                    current_steps + 1,
                )
        for neighbor in {(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)}:
            if grid[neighbor] is None:
                continue
            if grid[neighbor] == "#":
                explore_to_end(
                    steps_from_start,
                    cheat_savings,
                    cheat_savings_minimum,
                    neighbor,
                    current_steps + 1,
                )
    elif grid[r, c] == "#":
        for neighbor in {(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)}:
            if grid[neighbor] is None:
                continue
            if (
                grid[neighbor] in ".E"
                and neighbor in steps_from_start
                and steps_from_start[neighbor] - current_steps > cheat_savings_minimum
            ):
                cheat_savings.append(steps_from_start[neighbor] - current_steps)


steps_from_start = {}
cheat_savings = []
explore_to_end(steps_from_start, cheat_savings, 100, start, 0)
print(len(cheat_savings))


def manhattan(a, b):
    (ra, ca) = a
    (rb, cb) = b
    return abs(rb - ra) + abs(cb - ca)


good_cheats = 0
for cheat_start in steps_from_start:
    for cheat_end in steps_from_start:
        steps_delta = steps_from_start[cheat_end] - steps_from_start[cheat_start]
        distance_cost = manhattan(cheat_start, cheat_end)
        if steps_delta - distance_cost >= 100 and distance_cost <= 20:
            good_cheats += 1

print(good_cheats)
