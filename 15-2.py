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
        if grid_raw[r][c] == "#":
            grid[r, 2 * c] = "#"
            grid[r, 2 * c + 1] = "#"
        if grid_raw[r][c] == "O":
            grid[r, 2 * c] = "["
            grid[r, 2 * c + 1] = "]"
        if grid_raw[r][c] == ".":
            grid[r, 2 * c] = "."
            grid[r, 2 * c + 1] = "."
        if grid_raw[r][c] == "@":
            grid[r, 2 * c] = "@"
            grid[r, 2 * c + 1] = "."
            robot = (r, 2 * c)

# Debug:
columns *= 2
# out = ""
# for r in range(rows):
#     for c in range(columns):
#         out += grid[r, c]
#     out += "\n"
# print(out)
# input()


def move_frontier(rr, rc, dr, dc):
    global grid
    move_set = set()
    frontier = [(rr, rc)]
    while frontier:
        (r, c) = frontier.pop()
        if (r, c) in move_set or grid[r, c] == ".":
            continue
        move_set.add((r, c))
        if grid[r, c] == "[":
            frontier.append((r, c + 1))
        elif grid[r, c] == "]":
            frontier.append((r, c - 1))
        if grid[r + dr, c + dc] == "#":
            return (rr, rc)
        frontier.append((r + dr, c + dc))

    grid_saved = {}
    for r, c in move_set:
        grid_saved[r, c] = grid[r, c]
        grid[r, c] = "."
    for r, c in move_set:
        grid[r + dr, c + dc] = grid_saved[r, c]
    return (rr + dr, rc + dc)


# Debug:
# out = ""
# for r in range(rows):
#     for c in range(columns):
#         out += grid[r, c]
#     out += "\n"
# print(out)
# input()

for move in moves:
    (rr, rc) = robot
    if move == ">":
        robot = move_frontier(rr, rc, 0, 1)
    elif move == "<":
        robot = move_frontier(rr, rc, 0, -1)
    elif move == "v":
        robot = move_frontier(rr, rc, 1, 0)
    elif move == "^":
        robot = move_frontier(rr, rc, -1, 0)

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
    if grid[r, c] == "[":
        total += 100 * r + c

print(total)
