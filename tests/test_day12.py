import pytest

from aoc.day12 import *


def parse_moon(s):
    m = re.match(r"^pos=(<[^>]+>), vel=(<[^>]+>)$", s)
    return Moon(*parse_coord(m.group(1)), *parse_coord(m.group(2)))


def moon_iteration(*moon_strs):
    return tuple(parse_moon(moon_str) for moon_str in moon_strs)


def test_parse_moon():
    moon = Moon.from_str("<x=16, y=-11, z=2>")
    assert moon.x == 16
    assert moon.y == -11
    assert moon.z == 2
    assert moon.dx == 0
    assert moon.dy == 0
    assert moon.dz == 0


def test_moon_energy():
    moon = Moon(1, 2, 3, 4, 5, 6)
    assert moon.energy == 6 * 15


@pytest.mark.parametrize(
    "moon_iterations",
    [
        {
            0: moon_iteration(
                "pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>",
                "pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>",
                "pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>",
                "pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>",
            ),
            1: moon_iteration(
                "pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>",
                "pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>",
                "pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>",
                "pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>",
            ),
            2: moon_iteration(
                "pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>",
                "pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>",
                "pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>",
                "pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>",
            ),
            3: moon_iteration(
                "pos=<x= 5, y=-6, z=-1>, vel=<x= 0, y=-3, z= 0>",
                "pos=<x= 0, y= 0, z= 6>, vel=<x=-1, y= 2, z= 4>",
                "pos=<x= 2, y= 1, z=-5>, vel=<x= 1, y= 5, z=-4>",
                "pos=<x= 1, y=-8, z= 2>, vel=<x= 0, y=-4, z= 0>",
            ),
            4: moon_iteration(
                "pos=<x= 2, y=-8, z= 0>, vel=<x=-3, y=-2, z= 1>",
                "pos=<x= 2, y= 1, z= 7>, vel=<x= 2, y= 1, z= 1>",
                "pos=<x= 2, y= 3, z=-6>, vel=<x= 0, y= 2, z=-1>",
                "pos=<x= 2, y=-9, z= 1>, vel=<x= 1, y=-1, z=-1>",
            ),
            5: moon_iteration(
                "pos=<x=-1, y=-9, z= 2>, vel=<x=-3, y=-1, z= 2>",
                "pos=<x= 4, y= 1, z= 5>, vel=<x= 2, y= 0, z=-2>",
                "pos=<x= 2, y= 2, z=-4>, vel=<x= 0, y=-1, z= 2>",
                "pos=<x= 3, y=-7, z=-1>, vel=<x= 1, y= 2, z=-2>",
            ),
            6: moon_iteration(
                "pos=<x=-1, y=-7, z= 3>, vel=<x= 0, y= 2, z= 1>",
                "pos=<x= 3, y= 0, z= 0>, vel=<x=-1, y=-1, z=-5>",
                "pos=<x= 3, y=-2, z= 1>, vel=<x= 1, y=-4, z= 5>",
                "pos=<x= 3, y=-4, z=-2>, vel=<x= 0, y= 3, z=-1>",
            ),
            7: moon_iteration(
                "pos=<x= 2, y=-2, z= 1>, vel=<x= 3, y= 5, z=-2>",
                "pos=<x= 1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>",
                "pos=<x= 3, y=-7, z= 5>, vel=<x= 0, y=-5, z= 4>",
                "pos=<x= 2, y= 0, z= 0>, vel=<x=-1, y= 4, z= 2>",
            ),
            8: moon_iteration(
                "pos=<x= 5, y= 2, z=-2>, vel=<x= 3, y= 4, z=-3>",
                "pos=<x= 2, y=-7, z=-5>, vel=<x= 1, y=-3, z=-1>",
                "pos=<x= 0, y=-9, z= 6>, vel=<x=-3, y=-2, z= 1>",
                "pos=<x= 1, y= 1, z= 3>, vel=<x=-1, y= 1, z= 3>",
            ),
            9: moon_iteration(
                "pos=<x= 5, y= 3, z=-4>, vel=<x= 0, y= 1, z=-2>",
                "pos=<x= 2, y=-9, z=-3>, vel=<x= 0, y=-2, z= 2>",
                "pos=<x= 0, y=-8, z= 4>, vel=<x= 0, y= 1, z=-2>",
                "pos=<x= 1, y= 1, z= 5>, vel=<x= 0, y= 0, z= 2>",
            ),
            10: moon_iteration(
                "pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>",
                "pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>",
                "pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>",
                "pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>",
            ),
        },
        {
            0: moon_iteration(
                "pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>",
                "pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>",
                "pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>",
                "pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>",
            ),
            10: moon_iteration(
                "pos=<x= -9, y=-10, z=  1>, vel=<x= -2, y= -2, z= -1>",
                "pos=<x=  4, y= 10, z=  9>, vel=<x= -3, y=  7, z= -2>",
                "pos=<x=  8, y=-10, z= -3>, vel=<x=  5, y= -1, z= -2>",
                "pos=<x=  5, y=-10, z=  3>, vel=<x=  0, y= -4, z=  5>",
            ),
            20: moon_iteration(
                "pos=<x=-10, y=  3, z= -4>, vel=<x= -5, y=  2, z=  0>",
                "pos=<x=  5, y=-25, z=  6>, vel=<x=  1, y=  1, z= -4>",
                "pos=<x= 13, y=  1, z=  1>, vel=<x=  5, y= -2, z=  2>",
                "pos=<x=  0, y=  1, z=  7>, vel=<x= -1, y= -1, z=  2>",
            ),
            30: moon_iteration(
                "pos=<x= 15, y= -6, z= -9>, vel=<x= -5, y=  4, z=  0>",
                "pos=<x= -4, y=-11, z=  3>, vel=<x= -3, y=-10, z=  0>",
                "pos=<x=  0, y= -1, z= 11>, vel=<x=  7, y=  4, z=  3>",
                "pos=<x= -3, y= -2, z=  5>, vel=<x=  1, y=  2, z= -3>",
            ),
            40: moon_iteration(
                "pos=<x= 14, y=-12, z= -4>, vel=<x= 11, y=  3, z=  0>",
                "pos=<x= -1, y= 18, z=  8>, vel=<x= -5, y=  2, z=  3>",
                "pos=<x= -5, y=-14, z=  8>, vel=<x=  1, y= -2, z=  0>",
                "pos=<x=  0, y=-12, z= -2>, vel=<x= -7, y= -3, z= -3>",
            ),
            50: moon_iteration(
                "pos=<x=-23, y=  4, z=  1>, vel=<x= -7, y= -1, z=  2>",
                "pos=<x= 20, y=-31, z= 13>, vel=<x=  5, y=  3, z=  4>",
                "pos=<x= -4, y=  6, z=  1>, vel=<x= -1, y=  1, z= -3>",
                "pos=<x= 15, y=  1, z= -5>, vel=<x=  3, y= -3, z= -3>",
            ),
            60: moon_iteration(
                "pos=<x= 36, y=-10, z=  6>, vel=<x=  5, y=  0, z=  3>",
                "pos=<x=-18, y= 10, z=  9>, vel=<x= -3, y= -7, z=  5>",
                "pos=<x=  8, y=-12, z= -3>, vel=<x= -2, y=  1, z= -7>",
                "pos=<x=-18, y= -8, z= -2>, vel=<x=  0, y=  6, z= -1>",
            ),
            70: moon_iteration(
                "pos=<x=-33, y= -6, z=  5>, vel=<x= -5, y= -4, z=  7>",
                "pos=<x= 13, y= -9, z=  2>, vel=<x= -2, y= 11, z=  3>",
                "pos=<x= 11, y= -8, z=  2>, vel=<x=  8, y= -6, z= -7>",
                "pos=<x= 17, y=  3, z=  1>, vel=<x= -1, y= -1, z= -3>",
            ),
            80: moon_iteration(
                "pos=<x= 30, y= -8, z=  3>, vel=<x=  3, y=  3, z=  0>",
                "pos=<x= -2, y= -4, z=  0>, vel=<x=  4, y=-13, z=  2>",
                "pos=<x=-18, y= -7, z= 15>, vel=<x= -8, y=  2, z= -2>",
                "pos=<x= -2, y= -1, z= -8>, vel=<x=  1, y=  8, z=  0>",
            ),
            90: moon_iteration(
                "pos=<x=-25, y= -1, z=  4>, vel=<x=  1, y= -3, z=  4>",
                "pos=<x=  2, y= -9, z=  0>, vel=<x= -3, y= 13, z= -1>",
                "pos=<x= 32, y= -8, z= 14>, vel=<x=  5, y= -4, z=  6>",
                "pos=<x= -1, y= -2, z= -8>, vel=<x= -3, y= -6, z= -9>",
            ),
            100: moon_iteration(
                "pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>",
                "pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>",
                "pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>",
                "pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>",
            ),
        },
    ],
)
def test_timeline(moon_iterations):
    assert moon_iterations
    space_timeline = SpaceTimeline(moon_iterations[0])
    for i, moons in moon_iterations.items():
        assert space_timeline[i] == moons


@pytest.mark.parametrize(
    "moons, cycle_time",
    [
        (
            moon_iteration(
                "pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>",
                "pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>",
                "pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>",
                "pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>",
            ),
            2772,
        ),
        (
            moon_iteration(
                "pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>",
                "pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>",
                "pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>",
                "pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>",
            ),
            4686774924,
        ),
    ],
)
def test_cycle_detection(moons, cycle_time):
    assert SpaceTimeline(moons).cycle_len() == cycle_time


def test_solve():
    assert solve("data/day12.txt") == (10055, 374307970285176)
