# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("6.txt", "r").read()
lines = input_value.split("\n")

guard_start = None
direction = (-1, 0)
grid = defaultdict(lambda: None)
for i in range(len(lines)):
    for j in range(len(lines[i])):
        grid[i, j] = lines[i][j]
        if lines[i][j] == "^":
            guard_start = (i, j)


def get_next_direction(direction):
    if direction == (-1, 0):
        return (0, 1)
    elif direction == (0, 1):
        return (1, 0)
    elif direction == (1, 0):
        return (0, -1)
    else:
        return (-1, 0)


def count_seen_positions(grid, guard_start, direction):
    guard = guard_start
    direction = direction

    seen_states = set()
    seen_positions = set()
    while grid[guard] is not None:
        if (guard, direction) in seen_states:
            return None
        seen_states.add((guard, direction))
        seen_positions.add(guard)
        (i, j) = guard
        (di, dj) = direction
        next_guard = (i + di, j + dj)
        if grid[next_guard] != "#":
            guard = next_guard
        else:
            direction = get_next_direction(direction)

    return len(seen_positions)


# Part 1:
print(count_seen_positions(grid, guard_start, direction))

# Part 2:
bad_obstacles = 0
for i, j in list(grid.keys()):
    if grid[i, j] == ".":
        grid[i, j] = "#"
        if count_seen_positions(grid, guard_start, direction) is None:
            bad_obstacles += 1
        grid[i, j] = "."

print(bad_obstacles)
