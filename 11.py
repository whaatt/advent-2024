# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from functools import cache

input_value = open("11.txt", "r").read().split("\n")[0]

stones = input_value.split(" ")
for i in range(25):
    new_stones = []
    for stone in stones:
        if stone == "0":
            new_stones.append("1")
        elif len(stone) % 2 == 0:
            new_stones.append(str(int(stone[: len(stone) // 2])))
            new_stones.append(str(int(stone[len(stone) // 2 :])))
        else:
            new_stones.append(str(int(stone) * 2024))
    stones = new_stones

print(len(stones))


@cache
def count_stones_from(stone, iterations_left):
    if iterations_left == 0:
        return 1
    if stone == "0":
        return count_stones_from("1", iterations_left - 1)
    elif len(stone) % 2 == 0:
        return count_stones_from(
            str(int(stone[: len(stone) // 2])), iterations_left - 1
        ) + count_stones_from(str(int(stone[len(stone) // 2 :])), iterations_left - 1)
    else:
        return count_stones_from(str(int(stone) * 2024), iterations_left - 1)


stones = input_value.split(" ")
print(sum(count_stones_from(stone, 75) for stone in stones))
