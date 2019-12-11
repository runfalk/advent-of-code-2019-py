from aoc.plane import Coord
from aoc.common import last
from aoc.day3 import follow, solve


def test_follow():
    assert len(list(follow(["R10"]))) == 10
    assert len(list(follow("R8,U5,L5,D3".split(",")))) == 21
    assert len(list(follow("U7,R6,D4,L4".split(",")))) == 21

    assert last(follow(["R10"])) == Coord(10, 0)
    assert last(follow("R8,U5,L5,D3".split(","))) == Coord(3, -2)
    assert last(follow("U7,R6,D4,L4".split(","))) == Coord(2, -3)


def test_solve():
    assert solve("data/day3.txt") == (1017, 11432)
