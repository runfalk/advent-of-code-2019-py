import pytest

from itertools import islice

from aoc.day24 import (
    evolve,
    evolve_recursive,
    get_biodiversity_rating,
    iter_neighbors_recursive,
    parse_lines,
    solve,
)
from aoc.common import Coord


def test_get_biodiversity_rating():
    assert get_biodiversity_rating(set()) == 0
    assert get_biodiversity_rating({Coord(0, 0)}) == 1

    lines = [
        ".....",
        ".....",
        ".....",
        "#....",
        ".#...",
    ]
    assert get_biodiversity_rating(parse_lines(lines)) == 2129920


@pytest.mark.parametrize(
    "coord, neighbors",
    [
        (
            Coord(0, 0),
            {(-1, Coord(2, 1)), (-1, Coord(1, 2)), (0, Coord(1, 0)), (0, Coord(0, 1))},
        ),
        (Coord(1, 1), {(0, n) for n in Coord(1, 1).iter_neighbors()}),
        (
            Coord(2, 1),
            {(0, Coord(1, 1)), (0, Coord(2, 0)), (0, Coord(3, 1))}
            | {(1, Coord(x, 0)) for x in range(5)},
        ),
        (
            Coord(2, 3),
            {(0, Coord(2, 4)), (0, Coord(1, 3)), (0, Coord(3, 3))}
            | {(1, Coord(x, 4)) for x in range(5)},
        ),
        (
            Coord(1, 2),
            {(0, Coord(0, 2)), (0, Coord(1, 1)), (0, Coord(1, 3))}
            | {(1, Coord(0, y)) for y in range(5)},
        ),
        (
            Coord(3, 2),
            {(0, Coord(4, 2)), (0, Coord(3, 1)), (0, Coord(3, 3))}
            | {(1, Coord(4, y)) for y in range(5)},
        ),
        (
            Coord(4, 4),
            {(0, Coord(3, 4)), (0, Coord(4, 3)), (-1, Coord(2, 3)), (-1, Coord(3, 2))},
        ),
    ],
)
def test_iter_neighbors_recursive(coord, neighbors):
    assert set(iter_neighbors_recursive(0, coord)) == neighbors


def test_evolve():
    first_generation = parse_lines(["....#", "#..#.", "#..##", "..#..", "#...."])
    expected_generations = [
        parse_lines(["#..#.", "####.", "###.#", "##.##", ".##.."]),
        parse_lines(["#####", "....#", "....#", "...#.", "#.###"]),
        parse_lines(["#....", "####.", "...##", "#.##.", ".##.#"]),
        parse_lines(["####.", "....#", "##..#", ".....", "##..."]),
    ]
    for gen, expected_gen in zip(evolve(first_generation), expected_generations):
        assert gen == expected_gen


def test_evolve_recursive():
    generation = {
        (0, bug) for bug in parse_lines(["....#", "#..#.", "#.?##", "..#..", "#...."])
    }
    gen_10 = next(islice(evolve_recursive(generation), 9, None))
    assert len(gen_10) == 99


def test_solve():
    assert solve("data/day24.txt") == (26840049, 1995)
