from itertools import count

from .plane import Coord


def lines_from_file(path):
    with open(path) as f:
        for line in f:
            # Remove trailing whitespace
            yield line.rstrip("\r\n")


def last(it):
    """Return the last value of the given iterator"""
    output = None
    for item in it:
        output = item
    return output


def iter_peek(it, include_last=False):
    it = iter(it)
    prev = next(it)

    for curr in it:
        yield (prev, curr)
        prev = curr

    if include_last:
        yield (prev, None)


def coords_as_str(coords):
    return dict_coords_as_str({c: True for c in coords}, {True: "#", None: " "})


def dict_coords_as_str(coords, colors, default_value=None):
    min_x = min(x for x, _ in coords)
    min_y = min(y for _, y in coords)

    translation = Coord(min_x, min_y)
    translated_coords = {
        Coord(*coord) - translation: value for coord, value in coords.items()
    }

    width = max(x + 1 for x, _ in translated_coords)
    height = max(y + 1 for _, y in translated_coords)

    return "\n".join(
        "".join(
            colors[translated_coords.get(Coord(x, y), default_value)]
            for x in range(width)
        )
        for y in range(height)
    )
