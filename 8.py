# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict
from math import gcd

input_value = open("8.txt", "r").read()
lines = input_value.split("\n")

grid = defaultdict(lambda: None)
antennas = set()
for r in range(len(lines)):
    for c in range(len(lines[r])):
        grid[r, c] = lines[r][c]
        if grid[r, c] != ".":
            antennas.add((r, c))

antinodes = set()
for r1, c1 in antennas:
    for r2, c2 in antennas:
        if r1 == r2 and c1 == c2:
            continue
        if grid[r1, c1] != grid[r2, c2]:
            continue
        dr = r2 - r1
        dc = c2 - c1
        anti_1 = (r1 - dr, c1 - dc)
        anti_2 = (r2 + dr, c2 + dc)
        if grid[anti_1] is not None:
            antinodes.add(anti_1)
        if grid[anti_2] is not None:
            antinodes.add(anti_2)

# Part 1:
print(len(antinodes))

antinodes = set()
for r1, c1 in antennas:
    for r2, c2 in antennas:
        if r1 == r2 and c1 == c2:
            continue
        if grid[r1, c1] != grid[r2, c2]:
            continue
        dr = r2 - r1
        dc = c2 - c1
        divisor = gcd(dr, dc)
        dr /= divisor
        dc /= divisor
        k = 0
        while grid[r1 + k * dr, c1 + k * dc] is not None:
            antinodes.add((r1 + k * dr, c1 + k * dc))
            k += 1
        k = 0
        while grid[r1 + k * dr, c1 + k * dc] is not None:
            antinodes.add((r1 + k * dr, c1 + k * dc))
            k -= 1

# Part 2:
print(len(antinodes))
