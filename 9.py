# pylint: skip-file
# mypy: ignore-errors
# flake8: noqa

files_raw = open("9.txt", "r").read()


def get_files(files_raw):
    files = []
    is_file = True
    id = 0
    for digit in files_raw:
        if is_file:
            files.append((int(digit), id, 0))
            id += 1
        else:
            files.append((int(digit), []))
        is_file = not is_file
    return files


def get_checksum(files):
    i = 0
    total = 0
    for file in files:
        if type(file[1]) == list:
            for sub_file in file[1]:
                (count, id) = sub_file
                for _ in range(count):
                    total += id * i
                    i += 1
            i += file[0]
        else:
            (count, id, used) = file
            for _ in range(count):
                total += id * i
                i += 1
            i += used
    return total


# Part 1:
files = get_files(files_raw)
next_free = 1
i = len(files) - 1
while i > -1 and next_free < len(files):
    if i <= next_free:
        break
    if type(files[i][1]) == list:
        i -= 1
        continue
    (left, id, used) = files[i]
    (size, space) = files[next_free]
    to_move = min(size, left)
    size -= to_move
    left -= to_move
    used += to_move

    space.append((to_move, id))
    files[i] = (left, files[i][1], used)
    files[next_free] = (size, space)
    if left == 0:
        i -= 1
    if size == 0:
        next_free += 2

print(get_checksum(files))

# Part 2:
files = get_files(files_raw)

i = len(files) - 1
while i > -1:
    if type(files[i][1]) == list:
        i -= 1
        continue
    (left, id, used) = files[i]
    next_free = None
    for j in range(1, i, 2):
        if files[j][0] >= left:
            next_free = j
            break
    if next_free is None:
        i -= 1
        continue
    (size, space) = files[next_free]
    to_move = min(size, left)
    size -= to_move
    left -= to_move
    used += to_move

    space.append((to_move, id))
    files[i] = (left, files[i][1], used)
    files[next_free] = (size, space)
    i -= 1

print(get_checksum(files))
