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
)


def print_answer(prefix, answer):
    if isinstance(answer, str) and "\n" in answer:
        for line in answer.split("\n"):
            print(prefix, line)
            prefix = " " * len(prefix)
    else:
        print(prefix, answer)


def main():
    if len(sys.argv) < 2:
        print("Usage: aoc <day> [args...]")
        exit(0)

    day = int(sys.argv[1])
    if day == 1:
        a, b = day1.solve(sys.argv[2])
    elif day == 2:
        a, b = day2.solve(sys.argv[2])
    elif day == 3:
        a, b = day3.solve(sys.argv[2])
    elif day == 4:
        a, b = day4.solve(int(sys.argv[2]), int(sys.argv[3]))
    elif day == 5:
        a, b = day5.solve(sys.argv[2])
    elif day == 6:
        a, b = day6.solve(sys.argv[2])
    elif day == 7:
        a, b = day7.solve(sys.argv[2])
    elif day == 8:
        a, b = day8.solve(sys.argv[2])
    elif day == 9:
        a, b = day9.solve(sys.argv[2])
    elif day == 10:
        a, b = day10.solve(sys.argv[2])
    elif day == 11:
        a, b = day11.solve(sys.argv[2])
    elif day == 12:
        try:
            a, b = day12.solve(sys.argv[2])
        except:
            import pdb

            pdb.post_mortem()
    elif day == 13:
        a, b = day13.solve(sys.argv[2])
    elif day == 14:
        a, b = day14.solve(sys.argv[2])
    else:
        print("No solution for the given day ({})".format(day))
        exit(1)

    print_answer("A:", a)
    if b is not None:
        print_answer("B:", b)
