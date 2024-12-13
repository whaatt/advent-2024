# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("12.txt", "r").read()
lines = input_value.split("\n")
rows = len(lines)
columns = len(lines[0])

grid = defaultdict(lambda: None)
for r in range(rows):
    for c in range(columns):
        grid[r, c] = lines[r][c]

# Region setup:
region = 0
for r, c in list(grid.keys()):
    if grid[r, c] is None:
        continue
    if type(grid[r, c]) == int:
        continue
    seen = set()
    stack = [(r, c)]
    while stack:
        (rx, cx) = stack.pop()
        seen.add((rx, cx))
        # DFS over region.
        for neighbor in {(rx - 1, cx), (rx + 1, cx), (rx, cx - 1), (rx, cx + 1)}:
            if (
                grid[neighbor] is None
                or grid[neighbor] != grid[rx, cx]
                or neighbor in seen
            ):
                continue
            stack.append(neighbor)
        grid[rx, cx] = region
    region += 1

# Part 1:
area = defaultdict(int)
perimeter = defaultdict(int)

for r, c in list(grid.keys()):
    if grid[r, c] is None:
        continue
    area[grid[r, c]] += 1
    for neighbor in {(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)}:
        if grid[neighbor] is None or grid[neighbor] != grid[r, c]:
            perimeter[grid[r, c]] += 1

print(sum(area[region] * perimeter[region] for region in area))


# Part 2:
def edge(x, y):
    return (min(x, y), max(x, y))


sides = defaultdict(int)
seen_regions = set()
for r, c in list(grid.keys()):
    if grid[r, c] is None:
        continue
    if grid[r, c] in seen_regions:
        continue
    seen_regions.add(grid[r, c])
    seen_positions = set()
    seen_edges = set()
    stack = [(r, c)]
    while stack:
        (rx, cx) = stack.pop()
        seen_positions.add((rx, cx))
        edge_neighbors = set()
        for neighbor in {(rx - 1, cx), (rx + 1, cx), (rx, cx - 1), (rx, cx + 1)}:
            if grid[neighbor] is None or grid[neighbor] != grid[rx, cx]:
                (neighbor_r, neighbor_c) = neighbor
                is_new_edge = True
                # Check edge line for seen edges (ugly).
                # An edge line continues as long as the interior of the edge is
                # equal to the start of the edge line but the exterior is not
                # equal to the start of the edge line:
                if rx == neighbor_r:
                    i = 0
                    while True:
                        if (
                            grid[rx - i, cx] == grid[rx, cx]
                            and edge((rx - i, cx), (neighbor_r - i, neighbor_c))
                            in seen_edges
                        ):
                            is_new_edge = False
                            break
                        if (
                            grid[rx - i, cx] != grid[rx, cx]
                            or grid[rx - i, cx] == grid[neighbor_r - i, neighbor_c]
                        ):
                            break
                        i += 1
                    i = 0
                    while True:
                        if (
                            grid[rx + i, cx] == grid[rx, cx]
                            and edge((rx + i, cx), (neighbor_r + i, neighbor_c))
                            in seen_edges
                        ):
                            is_new_edge = False
                            break
                        if (
                            grid[rx + i, cx] != grid[rx, cx]
                            or grid[rx + i, cx] == grid[neighbor_r + i, neighbor_c]
                        ):
                            break
                        i += 1
                else:  # cx == neighbor_c
                    is_new_edge = True
                    i = 0
                    while True:
                        if (
                            grid[rx, cx - i] == grid[rx, cx]
                            and edge((rx, cx - i), (neighbor_r, neighbor_c - i))
                            in seen_edges
                        ):
                            is_new_edge = False
                            break
                        if (
                            grid[rx, cx - i] != grid[rx, cx]
                            or grid[rx, cx - i] == grid[neighbor_r, neighbor_c - i]
                        ):
                            break
                        i += 1
                    i = 0
                    while True:
                        if (
                            grid[rx, cx + i] == grid[rx, cx]
                            and edge((rx, cx + i), (neighbor_r, neighbor_c + i))
                            in seen_edges
                        ):
                            is_new_edge = False
                            break
                        if (
                            grid[rx, cx + i] != grid[rx, cx]
                            or grid[rx, cx + i] == grid[neighbor_r, neighbor_c + i]
                        ):
                            break
                        i += 1
                # New edge happens if no seen edges were found on the edge line.
                if is_new_edge:
                    sides[grid[r, c]] += 1
                seen_edges.add(edge((rx, cx), neighbor))
        # DFS over region.
        for neighbor in {(rx - 1, cx), (rx + 1, cx), (rx, cx - 1), (rx, cx + 1)}:
            if grid[neighbor] == grid[rx, cx] and neighbor not in seen_positions:
                stack.append(neighbor)

print(sum(area[region] * sides[region] for region in area))
