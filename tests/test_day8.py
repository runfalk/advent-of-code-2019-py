import pytest

from aoc.day8 import checksum, iter_chunks, render, solve


# fmt: off
@pytest.mark.parametrize("size, it, expected", [
    (1, range(5), [[x] for x in range(5)]),
    (2, range(5), [[0, 1], [2, 3], [4]]),
])
# fmt: on
def test_iter_chunks(size, it, expected):
    output = [
        [y for y in x]
        for x in iter_chunks(size, it)
    ]
    assert output == expected


def test_checksum():
    assert checksum((3, 2), map(int, "123456789012")) == 1


def test_render():
    assert render((2, 2), map(int, "0222112222120000")) == " X\nX "


def test_solve():
    b = "\n".join((
        " XX  X   XX  X XXX  X   X",
        "X  X X   XX X  X  X X   X",
        "X     X X XX   XXX   X X ",
        "X      X  X X  X  X   X  ",
        "X  X   X  X X  X  X   X  ",
        " XX    X  X  X XXX    X  ",
    ))
    assert solve("data/day8.txt") == (2176, b)
