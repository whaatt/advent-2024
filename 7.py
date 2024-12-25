# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("7.txt", "r").read()
lines = input_value.split("\n")


def get_total(lines, is_part_2):
    total = 0
    for line in lines:
        [left, right] = line.split(": ")
        left = int(left)
        right = [int(item) for item in right.split(" ")]

        ops_stack = [(right[0], 1)]
        seen_states = set()
        while ops_stack:
            (value, next_index) = ops_stack.pop()
            if (value, next_index) in seen_states:
                continue
            seen_states.add((value, next_index))
            if next_index < len(right):
                ops_stack.append((value * right[next_index], next_index + 1))
                ops_stack.append((value + right[next_index], next_index + 1))
                if is_part_2:
                    ops_stack.append(
                        (int(str(value) + str(right[next_index])), next_index + 1)
                    )
            elif value == left:
                total += left
                break

    return total


# Part 1:
print(get_total(lines, False))

# Part 2:
print(get_total(lines, True))
