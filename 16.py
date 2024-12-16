# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

import heapq
from collections import defaultdict

input_value = open("16.txt", "r").read()
lines = input_value.split("\n")
rows = len(lines)
columns = len(lines[0])

grid = defaultdict(lambda: "#")
deer, end = None, None
for r in range(rows):
    for c in range(columns):
        grid[r, c] = lines[r][c]
        if grid[r, c] == "S":
            deer = (r, c)
        elif grid[r, c] == "E":
            end = (r, c)

start_state = (deer, (0, 1))
min_score_seen = defaultdict(lambda: float("inf"))
sources_for_min_score = defaultdict(set)
heap = [(0, start_state)]
heapq.heapify(heap)
min_score_seen[start_state] = 0

turn_cost = 1000
forward_cost = 1


def get_moves_with_cost(grid, state):
    moves = []
    (position, delta) = state
    if delta == (0, 1):
        moves.append((turn_cost, (position, (1, 0))))
        moves.append((turn_cost, (position, (-1, 0))))
    elif delta == (1, 0):
        moves.append((turn_cost, (position, (0, -1))))
        moves.append((turn_cost, (position, (0, 1))))
    elif delta == (0, -1):
        moves.append((turn_cost, (position, (-1, 0))))
        moves.append((turn_cost, (position, (1, 0))))
    else:  # delta == (-1, 0)
        moves.append((turn_cost, (position, (0, 1))))
        moves.append((turn_cost, (position, (0, -1))))
    (r, c) = position
    (dr, dc) = delta
    if grid[r + dr, c + dc] != "#":
        moves.append((forward_cost, ((r + dr, c + dc), delta)))
    return moves


while heap:
    (score, state) = heapq.heappop(heap)
    if state[0] == end:
        # Part 1:
        print(score)
        break
    for cost, next_state in get_moves_with_cost(grid, state):
        next_score = score + cost
        if next_score == min_score_seen[next_state]:
            sources_for_min_score[next_state].add(state)
        elif next_score < min_score_seen[next_state]:
            heapq.heappush(heap, (next_score, next_state))
            min_score_seen[next_state] = next_score
            sources_for_min_score[next_state] = {state}

seen_positions = set()
stack = [(end, delta) for delta in {(0, 1), (1, 0), (0, -1), (-1, 0)}]
while stack:
    current_state = stack.pop()
    (position, delta) = current_state
    seen_positions.add(position)
    if current_state == start_state:
        continue
    stack.extend(sources_for_min_score[current_state])

# Part 2:
print(len(seen_positions))
