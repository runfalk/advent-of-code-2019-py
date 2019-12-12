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
    coords = set(coords)
    min_x = min(x for x, _ in coords)
    min_y = min(y for _, y in coords)

    translation = Coord(min_x, min_y)
    translated_coords = {coord - translation for coord in coords}

    width = max(x + 1 for x, _ in translated_coords)
    height = max(y + 1 for _, y in translated_coords)

    colors = {
        True: "#",
        False: " ",
    }

    return "\n".join(
        "".join(colors[Coord(x, y) in translated_coords] for x in range(width))
        for y in range(height)
    )
