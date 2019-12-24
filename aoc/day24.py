from itertools import islice, product

from .common import lines_from_file
from .plane import Coord


# All coordinates within the grid
grid = {Coord(x, y) for y in range(5) for x in range(5)}


def parse_lines(lines):
    return {
        Coord(x, y)
        for y, line in enumerate(lines)
        for x, tile in enumerate(line)
        if tile == "#"
    }


def find_first_duplicate(seq):
    history = set()
    for v in seq:
        if v in history:
            return v
        history.add(v)


def get_biodiversity_rating(generation):
    width = 5
    return sum(2 ** (y * width + x) for x, y in generation)


def will_live(is_alive, num_neighbors):
    if is_alive:
        return num_neighbors == 1
    else:
        return 0 < num_neighbors < 3


def iter_neighbors_recursive(depth, coord):
    for n in coord.iter_neighbors():
        if n == Coord(2, 2):
            if coord == Coord(2, 1):
                # From the left
                yield from ((depth + 1, Coord(x, 0)) for x in range(5))
            elif coord == Coord(2, 3):
                # From the right
                yield from ((depth + 1, Coord(x, 4)) for x in range(5))
            elif coord == Coord(1, 2):
                # From above
                yield from ((depth + 1, Coord(0, y)) for y in range(5))
            elif coord == Coord(3, 2):
                # From below
                yield from ((depth + 1, Coord(4, y)) for y in range(5))
        elif n.y == -1:
            # Above
            yield (depth - 1, Coord(2, 1))
        elif n.y == 5:
            # Below
            yield (depth - 1, Coord(2, 3))
        elif n.x == -1:
            # Left of
            yield (depth - 1, Coord(1, 2))
        elif n.x == 5:
            # Right of
            yield (depth - 1, Coord(3, 2))
        else:
            yield (depth, n)


def evolve(generation):
    while generation:
        next_generation = {
            bug
            for bug in grid
            if will_live(
                is_alive=bug in generation,
                num_neighbors=sum(1 for n in bug.iter_neighbors() if n in generation),
            )
        }
        yield next_generation
        generation = next_generation


def evolve_recursive(generation):
    min_depth = min((l for l, _ in generation), default=0)
    max_depth = max((l for l, _ in generation), default=0)
    layered_grid = grid - {Coord(2, 2)}

    while generation:
        next_generation = set()
        for depth, bug in product(range(min_depth - 1, max_depth + 2), layered_grid):
            num_n = sum(
                1 for n in iter_neighbors_recursive(depth, bug) if n in generation
            )
            if will_live(is_alive=(depth, bug) in generation, num_neighbors=num_n):
                next_generation.add((depth, bug))
                min_depth = min(min_depth, depth)
                max_depth = max(max_depth, depth)
        yield next_generation
        generation = next_generation


def solve(path):
    generation = parse_lines(lines_from_file(path))
    generation_with_depth = {(0, bug) for bug in generation if bug != Coord(2, 2)}
    a = find_first_duplicate(map(get_biodiversity_rating, evolve(generation)))
    b = len(next(islice(evolve_recursive(generation_with_depth), 199, None)))
    return (a, b)
