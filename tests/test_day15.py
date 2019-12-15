import asyncio
import pytest

from aoc.plane import Coord
from aoc.day15 import explore_maze, Maze, solve
from aoc.intcode import load_program_from_file


@pytest.fixture
def intcode():
    return load_program_from_file("data/day15.txt")


@pytest.fixture
def maze_lines():
    # Produced from my personal day 15 input, "o" is start, "X" is goal
    return [
        " ##### ########### ##### ### ########### ",
        "#.....#...........#.....#...#...........#",
        " ##.#.#######.###.#.###.#.#.###########.#",
        "#...#.#.....#.#...#.#...#.#.........#...#",
        "#.###.#.###.#.###.#.#.###.#########.#.#.#",
        "#.#.#.#.#...#...#...#.#.....#.......#.#.#",
        "#.#.#.#.#.#####.#####.#.#####.#######.#.#",
        "#.#.....#.#.....#.....#.#.....#.......#.#",
        "#.#######.#.#####.#####.#.#####.#######.#",
        "#.......#...#...#...#...#...#...#.......#",
        "#.#####.#####.#.###.#.#####.###.#.###### ",
        "#.....#.#.#...#...#.#.#.....#...#.#.....#",
        " ######.#.#.#.#####.#.#.#####.###.#.###.#",
        "#...#...#.#.#.......#.#.....#.#.#.#.#...#",
        "#.#.#.###.#.#########.#####.#.#.#.#.#.## ",
        "#.#...#...#.#...#...#...#...#.#...#.#...#",
        "#.#######.#.#.#.#.#####.#.###.#.#######.#",
        "#...#...#...#.#...#.....#.#...#.#.....#.#",
        "#.#.#.#.#.###.#.###.#####.###.#.#.###.#.#",
        "#.#...#.#.#...#.#.......#.#...#...#.#.#.#",
        " ######.#.#.###.#.#####.#.#.#######.#.#.#",
        "#.......#.#...#.#...#o#.#.#.#...#...#.#.#",
        "#.#######.###.#####.#.###.#.###.#.#.#.#.#",
        "#...#...#...#.#.....#.#...#...#...#.#.#.#",
        "#.#.###.###.#.#.#####.#.#####.#.###.#.#.#",
        "#.#.#.....#...#.....#.#.#.....#.#.#...#.#",
        "#.#.#.#.#####.#####.#.#.###.###.#.#####.#",
        "#.#.#.#.#.....#.....#...#...#.#...#...#.#",
        "#.#.#.###.#####.#########.###.###.#.#.#.#",
        "#.#.#...#...#...#.....#.....#.....#.#.#.#",
        " ##.###.#.###.#####.#.###.#.#.#####.#.#.#",
        "#...#...#.#...#.....#...#.#.#.#.....#.#.#",
        "#.###.###.#.#####.#####.###.#.#.###.#.#.#",
        "#.#X......#.....#.#...#.....#.#...#.#...#",
        "#.######## ####.#.#.#.#######.###.#.###.#",
        "#.#.......#...#.#...#.#.#...#.#...#...#.#",
        "#.#.#####.#.#.#.#.###.#.#.#.#.#####.#.#.#",
        "#.#.#...#.#.#.#.#.#...#...#...#...#.#.#.#",
        "#.#.###.#.#.#.#.###.###.#######.#.###.#.#",
        "#.......#...#.......#...........#.....#.#",
        " ####### ### ####### ########### ##### # ",
    ]


@pytest.fixture
def maze_relative_origin(maze_lines):
    return next(
        Coord(x, y)
        for y, row in enumerate(maze_lines)
        for x, tile in enumerate(row)
        if tile == "o"
    )


@pytest.fixture
def maze_end(maze_lines, maze_relative_origin):
    return next(
        Coord(x, y) - maze_relative_origin
        for y, row in enumerate(maze_lines)
        for x, tile in enumerate(row)
        if tile == "X"
    )


@pytest.fixture
def maze(maze_lines, maze_relative_origin):
    return Maze(
        {
            Coord(x, y) - maze_relative_origin
            for y, row in enumerate(maze_lines)
            for x, tile in enumerate(row)
            if tile == "#"
        }
    )


def test_maze_exploration(intcode, maze, maze_end):
    assert asyncio.run(explore_maze(intcode)) == (maze, maze_end)


def test_maze_shortest_path(maze, maze_end):
    assert len(maze.shortest_path(Coord(0, 0), maze_end)) == 374


def test_maze_longest_shortest_path(maze, maze_end):
    assert len(maze.longest_shortest_path(maze_end)) == 482


def test_solve():
    return solve("data/day15.txt") == (374, 482)
