# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict, deque
from functools import cache

input_value = open("21.txt", "r").read()
lines = input_value.split("\n")

number_pad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]
number_grid = defaultdict(lambda: None)
number_to_position = defaultdict(lambda: None)
for r in range(len(number_pad)):
    for c in range(len(number_pad[r])):
        number_grid[r, c] = number_pad[r][c]
        if number_pad[r][c] is not None:
            number_to_position[number_pad[r][c]] = (r, c)

direction_pad = [
    [None, "^", "A"],
    ["<", "v", ">"],
]
direction_grid = defaultdict(lambda: None)
direction_to_position = defaultdict(lambda: None)
for r in range(len(direction_pad)):
    for c in range(len(direction_pad[r])):
        direction_grid[r, c] = direction_pad[r][c]
        if direction_pad[r][c] is not None:
            direction_to_position[direction_pad[r][c]] = (r, c)


@cache
def get_shortest_numeric_paths(start_button, end_button):
    paths = set()
    queue = deque()
    queue.append(("", number_to_position[start_button]))
    end_position = number_to_position[end_button]
    while queue:
        (buttons, position) = queue.pop()
        (rc, cc) = position
        (re, ce) = end_position
        if position == end_position:
            paths.add(buttons + "A")
            continue
        if re > rc and number_grid[rc + 1, cc] is not None:
            queue.append((buttons + "v", (rc + 1, cc)))
        if re < rc and number_grid[rc - 1, cc] is not None:
            queue.append((buttons + "^", (rc - 1, cc)))
        if ce > cc and number_grid[rc, cc + 1] is not None:
            queue.append((buttons + ">", (rc, cc + 1)))
        if ce < cc and number_grid[rc, cc - 1] is not None:
            queue.append((buttons + "<", (rc, cc - 1)))
    return paths


@cache
def get_shortest_directional_paths(start_button, end_button):
    paths = set()
    queue = deque()
    queue.append(("", direction_to_position[start_button]))
    end_position = direction_to_position[end_button]
    while queue:
        (buttons, position) = queue.pop()
        (rc, cc) = position
        (re, ce) = end_position
        if position == end_position:
            paths.add(buttons + "A")
            continue
        if re > rc and direction_grid[rc + 1, cc] is not None:
            queue.append((buttons + "v", (rc + 1, cc)))
        if re < rc and direction_grid[rc - 1, cc] is not None:
            queue.append((buttons + "^", (rc - 1, cc)))
        if ce > cc and direction_grid[rc, cc + 1] is not None:
            queue.append((buttons + ">", (rc, cc + 1)))
        if ce < cc and direction_grid[rc, cc - 1] is not None:
            queue.append((buttons + "<", (rc, cc - 1)))
    return paths


# def expand_level(path_function, case, start_button="A"):
#     paths = None
#     current_button = start_button
#     for button in case:
#         edge_paths = path_function(current_button, button)
#         if paths is None:
#             new_paths = edge_paths
#         else:
#             new_paths = set()
#             for path in paths:
#                 for edge_path in edge_paths:
#                     new_paths.add(path + edge_path)
#         paths = new_paths
#         current_button = button
#     return paths


# total = 0
# for case in lines:
#     paths_numeric = expand_level(get_shortest_numeric_paths, case)
#     paths_directional = set()
#     for case_numeric in paths_numeric:
#         paths_directional |= expand_level(get_shortest_directional_paths, case_numeric)
#     paths_directional_2 = set()
#     for case_directional in paths_directional:
#         paths_directional_2 |= expand_level(
#             get_shortest_directional_paths, case_directional
#         )
#     total += min(len(path) for path in paths_directional_2) * int(case[:-1])

# # Part 1:
# print(total)


# Cache Size: O(2 * 25 * 10 * 10).
@cache
def get_best_score_for_motion_press(
    version, robot_levels_below, start_button, end_press_button
):
    if version == "numeric":
        paths = get_shortest_numeric_paths(start_button, end_press_button)
    else:
        paths = get_shortest_directional_paths(start_button, end_press_button)

    if robot_levels_below == 0:
        return len(next(iter(paths)))

    best_score = float("inf")
    for path in paths:
        score = 0
        path_with_start = "A" + path
        for i in range(len(path_with_start[:-1])):
            score += get_best_score_for_motion_press(
                "directional",
                robot_levels_below - 1,
                path_with_start[i],
                path_with_start[i + 1],
            )
        best_score = min(best_score, score)

    return best_score


def get_case_score(case, robot_levels_below):
    case_with_start = "A" + case
    case_score = 0
    for i in range(len(case_with_start[:-1])):
        case_score += get_best_score_for_motion_press(
            "numeric", robot_levels_below, case_with_start[i], case_with_start[i + 1]
        )
    return case_score


def get_case_complexity(case, robot_levels_below):
    return get_case_score(case, robot_levels_below) * int(case[:-1])


# Part 1 (Optimized):
print(sum(get_case_complexity(case, 2) for case in lines))

# Part 2:
print(sum(get_case_complexity(case, 25) for case in lines))
