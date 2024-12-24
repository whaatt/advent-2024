# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

from collections import defaultdict

input_value = open("24.txt", "r").read()
[inputs, gates] = input_value.split("\n\n")
inputs_raw = inputs.split("\n")
gates_raw = gates.split("\n")

name_to_value = defaultdict(lambda: None)
parent_gate = defaultdict(lambda: None)
parent_gate_op_name = defaultdict(lambda: None)
for input_raw in inputs_raw:
    [name, value] = input_raw.split(": ")
    name_to_value[name] = int(value)
    parent_gate[name] = None
    parent_gate_op_name[name] = None

op_name_to_op = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
}

for gate_raw in gates_raw:
    [lhs, output_name] = gate_raw.split(" -> ")
    [parent_1, op_name, parent_2] = lhs.split(" ")
    op = op_name_to_op[op_name]
    parent_gate[output_name] = (parent_1, op, parent_2)
    parent_gate_op_name[output_name] = (parent_1, op_name, parent_2)


# Manual memoization.
def get_value_for_name(cache, name):
    if cache[name] is not None:
        return cache[name]
    if name_to_value[name] is not None:
        cache[name] = name_to_value[name]
        return name_to_value[name]
    if parent_gate[name] is None:
        cache[name] = None
        return None

    (parent_1, op, parent_2) = parent_gate[name]
    value = op(get_value_for_name(cache, parent_1), get_value_for_name(cache, parent_2))
    cache[name] = value
    return value


def get_value_for_prefix(cache, prefix):
    output = 0
    multiplier = 1
    prefix_names = sorted(name for name in parent_gate if name[0] == prefix)
    for prefix_name in prefix_names:
        output += get_value_for_name(cache, prefix_name) * multiplier
        multiplier *= 2
    return output


def get_tuple_for_name(name):
    if name_to_value[name] is not None:
        return name
    if parent_gate[name] is None:
        return None

    (parent_1, op_name, parent_2) = parent_gate_op_name[name]
    return (name, get_tuple_for_name(parent_1), op_name, get_tuple_for_name(parent_2))


def normalize_tuple(value):
    if type(value) == str:
        return value, value, 0
    (name, lhs, op_name, rhs) = value
    lhs, lhs_smallest, lhs_depth = normalize_tuple(lhs)
    rhs, rhs_smallest, rhs_depth = normalize_tuple(rhs)
    if (lhs_smallest, lhs_depth) < (rhs_smallest, rhs_depth):
        return (name, lhs, op_name, rhs), lhs_smallest, max(lhs_depth, rhs_depth) + 1
    else:
        return (name, rhs, op_name, lhs), rhs_smallest, max(lhs_depth, rhs_depth) + 1


def tuple_deep_equal(first, second):  # Pass actual as second.
    if type(first) == str or type(second) == str:
        return first == second, None

    (_, first_lhs, first_op, first_rhs) = first
    (name, second_lhs, second_op, second_rhs) = second

    if first_op != second_op:
        return False, name
    lhs_good, error_source = tuple_deep_equal(first_lhs, second_lhs)
    if not lhs_good:
        return False, error_source or name
    rhs_good, error_source = tuple_deep_equal(first_rhs, second_rhs)
    if not rhs_good:
        return False, error_source or name
    return True, None


# Part 1:
print(get_value_for_prefix(defaultdict(lambda: None), "z"))

# C[0] = 0
# C[1] = X[0] & Y[0]
# C[i] = (C[i - 1] & (X[i - 1] ^ Y[i - 1])) | (X[i - 1] & Y[i - 1])
# Z[i] = C[i] ^ (X[i] ^ Y[i])


def make_expected_carry(i):
    if i == 0:
        return None
    if i == 1:
        return ("", "x00", "AND", "y00")
    return (
        "",
        (
            "",
            make_expected_carry(i - 1),
            "AND",
            ("", f"x{i-1:02}", "XOR", f"y{i-1:02}"),
        ),
        "OR",
        ("", f"x{i-1:02}", "AND", f"y{i-1:02}"),
    )


def make_expected_tuple(i):
    if i == 0:
        return ("", "x00", "XOR", "y00")
    return ("", make_expected_carry(i), "XOR", ("", f"x{i:02}", "XOR", f"y{i:02}"))


def get_normalized_actual_tuple(i):
    return normalize_tuple(get_tuple_for_name(f"z{i:02}"))[0]


# z_names = sorted(name for name in parent_gate if name[0] == "z")
# for i in range(len(z_names)):
#     print(i, tuple_deep_equal(make_expected_tuple(i), get_normalized_actual_tuple(i)))

# Part 2 (Manual Analysis):
print(",".join(sorted("frn z05 wnf vtj z21 gmq wtt z39".split(" "))))
