from itertools import count, islice

from .common import coords_as_str
from .day9 import Interpreter
from .intcode import load_program_from_file
from .plane import Coord


def query_pos(intcode, coord):
    return next(Interpreter.run_program(intcode, [coord.x, coord.y]))


def iter_lines(intcode):
    prev_start_x = 0
    prev_end_x = 1

    # Start at line 6 to ensure that we really get a beam
    for y in count():
        start_x = prev_start_x
        while not query_pos(intcode, Coord(start_x, y)):
            # This happens for lines that don't have any beam positions
            if start_x > prev_end_x:
                start_x = None
                break
            start_x += 1

        # Skip if we didn't find a beam
        if start_x is None:
            continue

        end_x = max(start_x, prev_end_x)
        while query_pos(intcode, Coord(end_x, y)):
            end_x += 1

        yield (Coord(start_x, y), Coord(end_x, y))

        prev_start_x = start_x
        prev_end_x = end_x


def query_area(intcode, width, height):
    beam = set()
    for start, end in iter_lines(intcode):
        if start.y >= height:
            break

        for x in range(start.x, end.x):
            if x >= width:
                break
            beam.add(Coord(x, start.y))
    return beam


def find_square(intcode, size):
    lines = iter_lines(intcode)
    history = [l for l in islice(lines, size - 1)]

    for i in count():
        offset = i % (size - 1)
        start, end = next(lines)
        old_start, old_end = history[offset]
        history[offset] = start, end

        square_corner = Coord(start.x, old_end.y)
        if square_corner.x + size <= old_end.x:
            return square_corner


def solve(path):
    intcode = load_program_from_file(path)
    assert query_pos(intcode, Coord(0, 0)) == 1

    emitter_area = query_area(intcode, 50, 50)
    square_corner = find_square(intcode, 100)
    return (len(emitter_area), 10_000 * square_corner.x + square_corner.y)
