# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict, deque

input_value = open("18.txt", "r").read()
lines = input_value.split("\n")
rows = 71
columns = 71

# Cute outer loop to combine parts 1 and 2...
for i in range(1024, len(lines)):
    grid = defaultdict(lambda: "#")
    for r in range(rows):
        for c in range(columns):
            grid[r, c] = "."

    for line in lines[:i]:
        (c, r) = tuple(int(value) for value in line.split(","))
        grid[r, c] = "#"

    start = (0, 0)
    target = (70, 70)

    seen = set()
    queue = deque()
    queue.append((start, 0))
    steps_found = None
    while queue:
        ((r, c), steps) = queue.popleft()
        if (r, c) in seen:
            continue
        seen.add((r, c))
        if (r, c) == target:
            steps_found = steps
            break
        for nr, nc in {(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)}:
            if grid[nr, nc] != "#":
                queue.append(((nr, nc), steps + 1))

    # Part 1:
    if steps_found is not None and i == 1024:
        print(steps)
    # Part 2:
    elif steps_found is None:
        print(lines[i - 1])
        break
