# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

import numpy as np

input_value = open("13.txt", "r").read()
games = input_value.split("\n\n")

a_cost = 3
b_cost = 1


def solve_with_constant_added(constant):
    total = 0
    for i in range(len(games)):
        [a, b, prize] = games[i].split("\n")
        a = a.split(" ")
        a = np.asarray((int(a[2][2:-1]), int(a[3][2:])))
        b = b.split(" ")
        b = np.asarray((int(b[2][2:-1]), int(b[3][2:])))
        prize = prize.split(" ")
        prize = (
            np.asarray(
                (int(prize[1][2:-1]), int(prize[2][2:])),
            )
            + constant
        )
        matrix = np.vstack((a, b))
        [a, b] = prize @ np.linalg.inv(matrix)
        if abs(a - round(a)) < 1e-4 and abs(b - round(b)) < 1e-4:
            total += round(a) * a_cost + round(b) * b_cost
    return total


# Part 1:
print(solve_with_constant_added(0))

# Part 2:
print(solve_with_constant_added(10000000000000))
