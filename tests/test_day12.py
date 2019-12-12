import pytest

from aoc.day12 import *


def test_parse_moon():
    moon = Coord.from_str("<x=16, y=-11, z=2>")
    assert moon.x == 16
    assert moon.y == -11
    assert moon.z == 2


def test_moon_energy():
    moon = Moon(Coord(1, 2, 3), vel=Coord(4, 5, 6))
    assert moon.potential_energy == 6
    assert moon.kinetic_energy == 15
    assert moon.energy == 6 * 15


def test_solve():
    assert solve("data/day12.txt") == (10055, 374307970285176)
