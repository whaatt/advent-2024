# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict
from functools import cache

input_value = open("10.txt", "r").read()
lines = input_value.split("\n")
rows = len(lines)
columns = len(lines[0])

grid = defaultdict(lambda: None)
for r in range(rows):
    for c in range(columns):
        grid[r, c] = int(lines[r][c])

# Part 1:
total = 0
for r in range(rows):
    for c in range(columns):
        if grid[r, c] != 0:
            continue

        count = 0
        seen = set()
        stack = [(r, c)]
        while stack:
            (r1, c1) = stack.pop()
            seen.add((r1, c1))
            if grid[r1, c1] == 9:
                count += 1
                continue
            for neighbor in {(r1 - 1, c1), (r1 + 1, c1), (r1, c1 - 1), (r1, c1 + 1)}:
                if neighbor not in seen and grid[neighbor] == grid[r1, c1] + 1:
                    stack.append(neighbor)

        total += count

print(total)


@cache
def ways_from(r, c):
    if grid[r, c] == 9:
        return 1
    total = 0
    for neighbor in {(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)}:
        if grid[neighbor] == grid[r, c] + 1:
            total += ways_from(neighbor[0], neighbor[1])
    return total


# Part 2:
ways = 0
for r in range(rows):
    for c in range(columns):
        if grid[r, c] == 0:
            ways += ways_from(r, c)

print(ways)
