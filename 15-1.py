# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("15.txt", "r").read()
[grid_raw, moves] = input_value.split("\n\n")

grid_raw = grid_raw.split("\n")
rows = len(grid_raw)
columns = len(grid_raw[0])

moves = "".join(moves.split("\n"))
grid = defaultdict(lambda: "#")
robot = None
for r in range(rows):
    for c in range(columns):
        grid[r, c] = grid_raw[r][c]
        if grid[r, c] == "@":
            robot = (r, c)

for move in moves:
    (rr, rc) = robot
    if move == ">":
        end_c = rc
        while grid[rr, end_c] in "@O":
            end_c += 1
        if grid[rr, end_c] == ".":
            for c in range(end_c - 1, rc - 1, -1):
                grid[rr, c + 1] = grid[rr, c]
            grid[rr, rc] = "."
            robot = (rr, rc + 1)
    elif move == "<":
        end_c = rc
        while grid[rr, end_c] in "@O":
            end_c -= 1
        if grid[rr, end_c] == ".":
            for c in range(end_c + 1, rc + 1):
                grid[rr, c - 1] = grid[rr, c]
            grid[rr, rc] = "."
            robot = (rr, rc - 1)
    elif move == "v":
        end_r = rr
        while grid[end_r, rc] in "@O":
            end_r += 1
        if grid[end_r, rc] == ".":
            for r in range(end_r - 1, rr - 1, -1):
                grid[r + 1, rc] = grid[r, rc]
            grid[rr, rc] = "."
            robot = (rr + 1, rc)
    elif move == "^":
        end_r = rr
        while grid[end_r, rc] in "@O":
            end_r -= 1
        if grid[end_r, rc] == ".":
            for r in range(end_r + 1, rr + 1):
                grid[r - 1, rc] = grid[r, rc]
            grid[rr, rc] = "."
            robot = (rr - 1, rc)

    # Debug:
    # out = ""
    # for r in range(rows):
    #     for c in range(columns):
    #         out += grid[r, c]
    #     out += "\n"
    # print(out)
    # input()

total = 0
for r, c in grid:
    if grid[r, c] == "O":
        total += 100 * r + c

print(total)
