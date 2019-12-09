import pytest

from aoc.day1 import get_fuel_req, get_fuel_load_req, solve


@pytest.mark.parametrize(
    "mass, output", [(12, 2), (14, 2), (1969, 654), (100756, 33583),]
)
def test_get_fuel_req(mass, output):
    assert get_fuel_req(mass) == output


@pytest.mark.parametrize(
    "mass, output", [(12, 2), (14, 2), (1969, 966), (100756, 50346),]
)
def test_get_fuel_load_req(mass, output):
    assert get_fuel_load_req(mass) == output


def test_solve():
    assert solve("data/day1.txt") == (3481005, 5218616)
