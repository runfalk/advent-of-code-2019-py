import sys

from . import (
    day1,
    day2,
    day3,
    day4,
    day5,
    day6,
    day7,
    day8,
    day9,
    day10,
    day11,
    day12,
    day13,
    day14,
    day15,
    day16,
    day17,
    day18,
    day19,
    day20,
    day21,
    day22,
    day23,
    day24,
    day25,
)


days = {
    1: day1.solve,
    2: day2.solve,
    3: day3.solve,
    4: day4.solve,
    5: day5.solve,
    6: day6.solve,
    7: day7.solve,
    8: day8.solve,
    9: day9.solve,
    10: day10.solve,
    11: day11.solve,
    12: day12.solve,
    13: day13.solve,
    14: day14.solve,
    15: day15.solve,
    16: day16.solve,
    17: day17.solve,
    18: day18.solve,
    19: day19.solve,
    20: day20.solve,
    21: day21.solve,
    22: day22.solve,
    23: day23.solve,
    24: day24.solve,
    25: day25.solve,
}


def print_answer(prefix, answer):
    if isinstance(answer, str) and "\n" in answer:
        for line in answer.split("\n"):
            print(prefix, line)
            prefix = " " * len(prefix)
    else:
        print(prefix, answer)


def main():
    argc = len(sys.argv)
    if argc < 2 or argc > 3:
        print("Usage: aoc <day> [input-file]")
        exit(0)

    day = int(sys.argv[1])
    solver = days.get(day, None)
    if solver is None:
        print("No solution for the given day ({})".format(day))
        exit(1)

    path = f"data/day{day}.txt"
    if argc == 3:
        path = sys.argv[2]

    a, b = solver(path)
    print_answer("A:", a)
    if b is not None:
        print_answer("B:", b)
