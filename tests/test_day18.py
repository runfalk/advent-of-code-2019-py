import pytest

from aoc.day18 import find_paths, solve, tsp_solve


@pytest.mark.parametrize(
    "steps, maze_lines",
    [
        (8, ["#########", "#b.A.@.a#", "#########",],),
        (
            86,
            [
                "########################",
                "#f.D.E.e.C.b.A.@.a.B.c.#",
                "######################.#",
                "#d.....................#",
                "########################",
            ],
        ),
        (
            81,
            [
                "########################",
                "#@..............ac.GI.b#",
                "###d#e#f################",
                "###A#B#C################",
                "###g#h#i################",
                "########################",
            ],
        ),
        (
            136,
            [
                "#################",
                "#i.G..c...e..H.p#",
                "########.########",
                "#j.A..b...f..D.o#",
                "########@########",
                "#k.E..a...g..B.n#",
                "########.########",
                "#l.F..d...h..C.m#",
                "#################",
            ],
        ),
        (
            24,
            [
                "###############",
                "#d.ABC.#.....a#",
                "######@#@######",
                "###############",
                "######@#@######",
                "#b.....#.....c#",
                "###############",
            ],
        ),
        (
            32,
            [
                "#############",
                "#DcBa.#.GhKl#",
                "#.###@#@#I###",
                "#e#d#####j#k#",
                "###C#@#@###J#",
                "#fEbA.#.FgHi#",
                "#############",
            ],
        ),
        (
            72,
            [
                "#############",
                "#g#f.D#..h#l#",
                "#F###e#E###.#",
                "#dCba@#@BcIJ#",
                "#############",
                "#nK.L@#@G...#",
                "#M###N#H###.#",
                "#o#m..#i#jk.#",
                "#############",
            ],
        ),
    ],
)
def test_tsp_solve(steps, maze_lines):
    graph = find_paths(maze_lines)
    assert tsp_solve(graph) == steps


def test_solve():
    assert solve("data/day18.txt") == (2946, 1222)