from aoc.day17 import iter_intersections, iter_patterns, solve
from aoc.plane import Coord


def test_iter_intersections():
    # +------+
    # |  # # |
    # | #X#X#|
    # |  # # |
    # +------+
    scaffolds = {
        Coord(2, 0),
        Coord(4, 0),
        Coord(1, 1),
        Coord(2, 1),
        Coord(3, 1),
        Coord(4, 1),
        Coord(5, 1),
        Coord(2, 2),
        Coord(4, 2),
    }
    assert set(iter_intersections(scaffolds)) == {Coord(2, 1), Coord(4, 1)}


def test_iter_patterns():
    l = [1, 2, 3, 4, 5]
    patterns = {
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 5),
        (1, 2, 3, 4),
        (2, 3, 4, 5),
        (1, 2, 3, 4, 5),
    }
    assert set(iter_patterns(l, min_len=4)) == {p for p in patterns if len(p) >= 4}
    assert set(iter_patterns(l)) == patterns


def test_solve():
    assert solve("data/day17.txt") == (7328, 1289413)
