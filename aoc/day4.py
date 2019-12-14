from itertools import groupby

from .common import iter_peek, lines_from_file


def is_sorted(seq):
    items = list(seq)
    return items == list(sorted(items))


def has_repetions(it):
    for c, n in iter_peek(it):
        if c == n:
            return True
    return False


def has_pairs(it):
    # Since we know the input is sorted we can use groupby()
    for _, streak in groupby(it):
        if len(list(streak)) == 2:
            return True
    return False


def is_pw(pw):
    if len(pw) != 6:
        return False
    elif not is_sorted(pw):
        return False
    return has_repetions(pw)


def solve(path):
    line, = lines_from_file(path)
    start, end = map(int, line.split("-"))

    a = 0
    b = 0

    for pw in range(start, end + 1):
        pw = str(pw)

        if not is_pw(pw):
            continue

        a += 1

        # Since part B is a subset of part A, we just have to perform the additional check
        if has_pairs(pw):
            b += 1

    return (a, b)
