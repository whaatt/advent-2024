# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict, deque
from functools import cache
from math import floor

input_value = open("22.txt", "r").read()
lines = input_value.split("\n")
secrets = [int(value) for value in lines]


def mix_with_secret(secret, value):
    return secret ^ value


def prune_secret(secret):
    return secret % 16777216


def get_next_secret(secret):
    result_1 = secret * 64
    secret = mix_with_secret(secret, result_1)
    secret = prune_secret(secret)

    result_2 = floor(secret / 32)
    secret = mix_with_secret(secret, result_2)
    secret = prune_secret(secret)

    result_3 = secret * 2048
    secret = mix_with_secret(secret, result_3)
    secret = prune_secret(secret)
    return secret


def get_next_secret_n(secret, n):
    for _ in range(n):
        secret = get_next_secret(secret)
    return secret


# Part 1:
print(sum(get_next_secret_n(secret, 2000) for secret in secrets))


def populate_price_totals(delta_price_totals, secret, n):
    deltas = deque()
    seen_deltas = set()
    for _ in range(n):
        next_secret = get_next_secret(secret)
        deltas.append(next_secret % 10 - secret % 10)
        if len(deltas) == 4:
            if tuple(deltas) not in seen_deltas:
                seen_deltas.add(tuple(deltas))
                delta_price_totals[tuple(deltas)] += next_secret % 10
            deltas.popleft()
        secret = next_secret


# Part 2:
delta_price_totals = defaultdict(int)
for secret in secrets:
    populate_price_totals(delta_price_totals, secret, 2000)
print(max(delta_price_totals.values()))
