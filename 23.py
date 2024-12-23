# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import Counter, defaultdict, deque
from functools import cache
from math import floor

input_value = open("23.txt", "r").read()
lines = input_value.split("\n")

edges = set()
adjacency = defaultdict(set)
for line in lines:
    edge = tuple(sorted(line.split("-")))
    edges.add(edge)
    (start, end) = edge
    adjacency[start].add(end)
    adjacency[end].add(start)

triples = set()
for edge in edges:
    (start, end) = edge
    mutuals = (adjacency[start] & adjacency[end]).difference({start, end})
    for mutual in mutuals:
        triples.add(tuple(sorted([start, end, mutual])))

count_target = 0
for triple in triples:
    for machine in triple:
        if machine[0] == "t":
            count_target += 1
            break

# Part 1:
print(count_target)


def find_largest_party_for_machine(adjacency, machine):
    seen_states = set()
    stack = [(machine, {machine})]
    largest_set = set()
    while stack:
        (current, current_set) = stack.pop()
        if current in seen_states:
            continue
        seen_states.add(current)
        if len(current_set) > len(largest_set):
            largest_set = current_set
        for neighbor in adjacency[current]:
            if neighbor in current_set:
                continue
            member_not_found = False
            for member in current_set:
                desired_edge = tuple((min(member, neighbor), max(member, neighbor)))
                if desired_edge not in edges:
                    member_not_found = True
                    break
            if member_not_found:
                continue
            stack.append((neighbor, current_set | {neighbor}))
    return largest_set


i = 0
largest_party = set()
for machine in adjacency:
    largest_party_for_machine = find_largest_party_for_machine(adjacency, machine)
    if len(largest_party_for_machine) > len(largest_party):
        largest_party = largest_party_for_machine
    i += 1

# Part 2:
print(",".join(sorted(largest_party)))
