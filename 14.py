# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("14.txt", "r").read()
lines = input_value.split("\n")

robots = []
for line in lines:
    line = line.split(" ")
    position = tuple(int(value) for value in line[0].split("=")[1].split(","))
    velocity = tuple(int(value) for value in line[1].split("=")[1].split(","))
    robots.append((position, velocity))

width = 101
height = 103

# Part 1:
iterations = 100
robots_1 = []
for i in range(len(robots)):
    ((px, py), (vx, vy)) = robots[i]
    px = (px + iterations * vx) % width
    py = (py + iterations * vy) % height
    robots_1.append(((px, py), (vx, vy)))

tl = sum(1 for ((px, py), _) in robots_1 if px < width // 2 and py < height // 2)
tr = sum(1 for ((px, py), _) in robots_1 if px >= width // 2 + 1 and py < height // 2)
bl = sum(1 for ((px, py), _) in robots_1 if px < width // 2 and py >= height // 2 + 1)
br = sum(
    1 for ((px, py), _) in robots_1 if px >= width // 2 + 1 and py >= height // 2 + 1
)
print(tl * tr * bl * br)

# Part 2:
seconds = 0
# Constant determined through empirical printing of grids at various iteration
# counts:
iterations = 6644
grid = defaultdict(int)
for i in range(len(robots)):
    ((px, py), (vx, vy)) = robots[i]
    px = (px + iterations * vx) % width
    py = (py + iterations * vy) % height
    grid[px, py] += 1
    robots[i] = ((px, py), (vx, vy))
grid_string = ""
for y in range(height):
    for x in range(width):
        if (x, y) in grid:
            grid_string += "#"
        else:
            grid_string += "."
    grid_string += "\n"
# print(grid_string)
print(iterations)
