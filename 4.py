# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("4.txt", "r").read()
lines = input_value.split("\n")

rows = len(lines)
columns = len(lines[0])
grid = defaultdict(
    str, {(i, j): lines[i][j] for i in range(rows) for j in range(columns)}
)


# Part 1:
def rays(i, j, t):
    return [
        [(i + dt, j) for dt in range(t)],
        [(i - dt, j) for dt in range(t)],
        [(i, j + dt) for dt in range(t)],
        [(i, j - dt) for dt in range(t)],
        [(i + dt, j + dt) for dt in range(t)],
        [(i + dt, j - dt) for dt in range(t)],
        [(i - dt, j + dt) for dt in range(t)],
        [(i - dt, j - dt) for dt in range(t)],
    ]


target = "XMAS"
count = 0

for i in range(rows):
    for j in range(columns):
        for ray in rays(i, j, len(target)):
            if target == "".join(grid[cell] for cell in ray):
                count += 1

print(count)


# Part 2:
def symmetric_diagonals(i, j, t):
    return [
        [(i + dt, j + dt) for dt in range(-t, t + 1)],
        [(i + dt, j - dt) for dt in range(-t, t + 1)],
    ]


targets = ["MAS", "SAM"]
count = 0

for i in range(rows):
    for j in range(columns):
        if all(
            "".join(grid[cell] for cell in diagonal) in targets
            for diagonal in symmetric_diagonals(i, j, 1)
        ):
            count += 1

print(count)
