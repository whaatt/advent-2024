# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("5.txt", "r").read()
[rules, orderings] = input_value.split("\n\n")
rules = [tuple(int(page) for page in rule.split("|")) for rule in rules.split("\n")]
orderings = [
    [int(page) for page in ordering.split(",")] for ordering in orderings.split("\n")
]

ordering_dicts = []
for ordering in orderings:
    ordering_dict = defaultdict(lambda: None)
    for i in range(len(ordering)):
        ordering_dict[ordering[i]] = i
    ordering_dicts.append(ordering_dict)

# Part 1:
total = 0
good_rows = set()
for i in range(len(orderings)):
    is_bad = False
    for rule in rules:
        index_first = ordering_dicts[i][rule[0]]
        index_second = ordering_dicts[i][rule[1]]
        if index_first is None or index_second is None:
            continue
        if index_first >= index_second:
            is_bad = True
            break
    if not is_bad:
        good_rows.add(i)
        total += orderings[i][len(orderings[i]) // 2]

print(total)

# Part 2:
i = 0
total = 0
while i < len(orderings):
    if i in good_rows:
        i += 1
        continue
    was_bad = False
    for rule in rules:
        index_first = ordering_dicts[i][rule[0]]
        index_second = ordering_dicts[i][rule[1]]
        if index_first is None or index_second is None:
            continue
        if index_first >= index_second:
            was_bad = True
            ordering_dicts[i][rule[0]] = index_second
            ordering_dicts[i][rule[1]] = index_first
            orderings[i][index_first], orderings[i][index_second] = (
                orderings[i][index_second],
                orderings[i][index_first],
            )
    if not was_bad:
        total += orderings[i][len(orderings[i]) // 2]
        i += 1

print(total)
