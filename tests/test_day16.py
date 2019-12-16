import pytest

from aoc.day16 import *


def test_split_digits():
    return join_digits(split_digits("01234")) == "01234"


def test_slice_cycle_list():
    l = list(range(10))
    offset = 1_000_000_000_000_000
    assert slice_cycled_list(l, offset, offset + len(l) * 2) == l * 2


@pytest.mark.parametrize(
    "msg, phase, output",
    [
        ("12345678", 1, "48226158"),
        ("48226158", 1, "34040438"),
        ("34040438", 1, "03415518"),
        ("03415518", 1, "01029498"),
        ("80871224585914546619083218645595", 100, "24176176"),
        ("19617804207202209144916044189917", 100, "73745418"),
        ("69317163492948606335995924319873", 100, "52432133"),
    ],
)
def test_calc_fft(msg, phase, output):
    assert len(output) == 8
    assert calc_fft(msg, phase) == output


@pytest.mark.parametrize(
    "msg, output",
    [
        ("03036732577212944063491565474664", "84462026"),
        ("02935109699940807407585447034323", "78725270"),
        ("03081770884921959731165446850517", "53553731"),
    ],
)
def test_calc_fast_fft(msg, output):
    assert calc_fast_fft(msg, 100) == output


@pytest.mark.parametrize(
    "phase, pattern, output",
    [
        (0, [0, 1, 0, -1], []),
        (1, [0, 1, 0, -1], [1, 0, -1, 0]),
        (2, [0, 1, 0, -1], [1, 1, 0, 0, -1, -1, 0, 0]),
    ],
)
def test_get_pattern(phase, pattern, output):
    assert list(islice(iter_pattern([0, 1, 0, -1], phase), len(output))) == output


def test_solve():
    assert solve("data/day16.txt") == ("58672132", "91689380")
