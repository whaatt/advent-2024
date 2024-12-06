# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

import re

message = open("3.txt", "r").read()

# Part 1:
pairs = re.findall(r"mul\((\d\d?\d?),(\d\d?\d?)\)", message)
print(sum(int(pair[0]) * int(pair[1]) for pair in pairs))

# Part 2:
items = re.findall(r"(do\(\))|(don't\(\))|mul\((\d\d?\d?),(\d\d?\d?)\)", message)
enabled = True
total = 0
for item in items:
    if item[0] != "":
        enabled = True
    elif item[1] != "":
        enabled = False
    elif enabled:
        total += int(item[2]) * int(item[3])
print(total)
