import pytest

from aoc.plane import Coord, Vector
from aoc.day10 import Map, solve, vector_angle


def test_vector_angle():
    assert vector_angle(Vector(0, -1)) < vector_angle(Vector(1, 0))
    assert vector_angle(Vector(1, 0)) < vector_angle(Vector(0, 1))
    assert vector_angle(Vector(0, 1)) < vector_angle(Vector(-1, -1))

    # Test angles close to the breaking point
    assert vector_angle(Vector(-1, -1000)) > vector_angle(Vector(1, -1000))


def test_get_rays():
    m = Map((x, y) for y in range(3) for x in range(3))
    rays = {(0, 1), (1, 0), (1, 1), (2, 1), (1, 2)}
    origin = (0, 2)
    assert rays == {tuple(next(ray.iter_coords(origin))) for ray in m.get_rays(origin)}


@pytest.mark.parametrize(
    "str_map, best_asteroid, num_detectables",
    [
        ([".#..#", ".....", "#####", "....#", "...##",], (3, 4), 8),
        (
            [
                "......#.#.",
                "#..#.#....",
                "..#######.",
                ".#.#.###..",
                ".#..#.....",
                "..#....#.#",
                "#..#....#.",
                ".##.#..###",
                "##...#..#.",
                ".#....####",
            ],
            (5, 8),
            33,
        ),
        (
            [
                "#.#...#.#.",
                ".###....#.",
                ".#....#...",
                "##.#.#.#.#",
                "....#.#.#.",
                ".##..###.#",
                "..#...##..",
                "..##....##",
                "......#...",
                ".####.###.",
            ],
            (1, 2),
            35,
        ),
        (
            [
                ".#..#..###",
                "####.###.#",
                "....###.#.",
                "..###.##.#",
                "##.##.#.#.",
                "....###..#",
                "..#.#..#.#",
                "#..#.#.###",
                ".##...##.#",
                ".....#.#..",
            ],
            (6, 3),
            41,
        ),
        (
            [
                ".#..##.###...#######",
                "##.############..##.",
                ".#.######.########.#",
                ".###.#######.####.#.",
                "#####.##.#.##.###.##",
                "..#####..#.#########",
                "####################",
                "#.####....###.#.#.##",
                "##.#################",
                "#####.##.###..####..",
                "..######..##.#######",
                "####.##.####...##..#",
                ".#####..#.######.###",
                "##...#.##########...",
                "#.##########.#######",
                ".####.#.###.###.#.##",
                "....##.##.###..#####",
                ".#.#.###########.###",
                "#.#.#.#####.####.###",
                "###.##.####.##.#..##",
            ],
            (11, 13),
            210,
        ),
    ],
)
def test_detectable_asteroids(str_map, best_asteroid, num_detectables):
    m = Map.from_lines(str_map)
    assert (Coord(*best_asteroid), num_detectables) == max(
        ((a, m.detectable_asteroids(a)) for a in m), key=lambda x: x[1],
    )


def test_spinning_laser():
    m = Map.from_lines(
        [
            ".#..##.###...#######",
            "##.############..##.",
            ".#.######.########.#",
            ".###.#######.####.#.",
            "#####.##.#.##.###.##",
            "..#####..#.#########",
            "####################",
            "#.####....###.#.#.##",
            "##.#################",
            "#####.##.###..####..",
            "..######..##.#######",
            "####.##.####...##..#",
            ".#####..#.######.###",
            "##...#.##########...",
            "#.##########.#######",
            ".####.#.###.###.#.##",
            "....##.##.###..#####",
            ".#.#.###########.###",
            "#.#.#.#####.####.###",
            "###.##.####.##.#..##",
        ]
    )

    destruction_order = list(m.iter_spinning_laser_targets((11, 13)))
    expected_order = {
        1: (11, 12),
        2: (12, 1),
        3: (12, 2),
        10: (12, 8),
        20: (16, 0),
        50: (16, 9),
        100: (10, 16),
        199: (9, 6),
        200: (8, 2),
        201: (10, 9),
        299: (11, 1),
    }
    for i, coord in expected_order.items():
        assert destruction_order[i - 1] == Coord(*coord)


def test_solve():
    assert solve("data/day10.txt") == (303, 408)
