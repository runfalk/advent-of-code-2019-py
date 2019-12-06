import sys

from . import day2, day4, day5, day6


def main():
    if len(sys.argv) < 2:
        print("Usage: aoc <day> [args...]")
        exit(0)

    day = int(sys.argv[1])
    if day == 2:
        a, b = day2.solve(sys.argv[2])
    elif day == 4:
        a, b = day4.solve(int(sys.argv[2]), int(sys.argv[3]))
    elif day == 5:
        a, b = day5.solve(sys.argv[2])
    elif day == 6:
        a, b = day6.solve(sys.argv[2])
    else:
        print("No solution for the given day ({})".format(day))
        exit(1)

    print("A:", a)
    if b is not None:
        print("B:", b)
