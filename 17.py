# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

input_value = open("17.txt", "r").read()
lines = input_value.split("\n")


def output_to_string(out):
    return ",".join(str(value) for value in out)


def run_program(program, A, B, C):
    out = []
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]

        # Calculate combo:
        if 0 <= operand <= 3:
            combo = operand
        elif operand == 4:
            combo = A
        elif operand == 5:
            combo = B
        elif operand == 6:
            combo = C

        # Calculate result:
        if opcode == 0:
            A = A // (2**combo)
        elif opcode == 1:
            B = B ^ operand
        elif opcode == 2:
            B = combo % 8
        elif opcode == 3:
            if A != 0:
                ip = operand
                continue
        elif opcode == 4:
            B = B ^ C
        elif opcode == 5:
            out.append(combo % 8)
        elif opcode == 6:
            B = A // (2**combo)
        elif opcode == 7:
            C = A // (2**combo)
        ip += 2

    return output_to_string(out)


A = int(lines[0].split(": ")[1])
B = int(lines[1].split(": ")[1])
C = int(lines[2].split(": ")[1])

# Part 1:
program = [int(value) for value in lines[4].split(": ")[1].split(",")]
print(run_program(program, A, B, C))


# Insight from program analysis is that the first digit output by the program
# repeats every 1024 values of A. Since A also divides itself by 8 on each go
# before an output is produced, at most on each go we will have to try 1024
# different additions at that "eightfold-multiplication-level."
def search_next(i, start):
    for delta in range(1024):
        if run_program(program, start + delta, B, C) == output_to_string(program[i:]):
            if i == 0:
                return start + delta
            result = search_next(i - 1, 8 * (start + delta))
            if result is not None:
                return result
    return None


# Part 2:
A_answer = search_next(len(program) - 1, 0)
assert run_program(program, A_answer, B, C) == output_to_string(program)
print(A_answer)
