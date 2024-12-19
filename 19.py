# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from functools import cache

input_value = open("19.txt", "r").read()
[towels, designs] = input_value.split("\n\n")

towels = set(towels.split(", "))
designs = designs.split("\n")


@cache
def ways_possible(suffix):
    if len(suffix) == 0:
        return 1
    ways_here = 0
    for end in range(1, len(suffix) + 1):
        needed_towel = suffix[:end]
        if needed_towel in towels:
            ways_here += ways_possible(suffix[end:])
    return ways_here


is_possible = 0
total_ways_possible = 0
for design in designs:
    ways_here = ways_possible(design)
    total_ways_possible += ways_here
    if ways_here > 0:
        is_possible += 1

# Part 1:
print(is_possible)

# Part 2:
print(total_ways_possible)
