from collections import Counter
from itertools import chain, islice

from .common import lines_from_file


def iter_chunks(size, it):
    it = iter(it)
    while True:
        chunk_iter = islice(it, size)
        try:
            # We need to check if there is at least one element in this chunk.
            # Otherwise we will return empty chunks for eternity once the inner
            # iterator is exhausted.
            first = next(chunk_iter)
            yield chain([first], chunk_iter)
        except StopIteration:
            break


def checksum(size, digits):
    digits_per_layer = size[0] * size[1]
    fewest_zeroes = min(
        (Counter(layer) for layer in iter_chunks(digits_per_layer, digits)),
        key=lambda x: x[0],
    )
    return fewest_zeroes[1] * fewest_zeroes[2]


def render(size, digits):
    layer_size = size[0] * size[1]
    # Setup a transparent canvas to draw on
    pixels = [2] * layer_size

    for layer in iter_chunks(layer_size, digits):
        for i, p in enumerate(layer):
            # Since the the first layers are on top we can only draw if the pixel
            # is transparent.
            if pixels[i] == 2:
                pixels[i] = p

    colors = {
        0: " ",  # Black
        1: "X",  # White
    }

    return "\n".join(
        "".join(colors[c] for c in row) for row in iter_chunks(size[0], pixels)
    )


def solve(path):
    digits = list(map(int, list(lines_from_file(path))[0]))
    size = (25, 6)
    return (
        checksum(size, digits),
        render(size, digits),
    )
