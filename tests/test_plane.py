import pytest

from aoc.plane import Coord, Vector


@pytest.mark.parametrize(
    "input, normalized",
    [
        ((1, 1), (1, 1)),
        ((2, 2), (1, 1)),
        ((9, 9), (1, 1)),
        ((4, 0), (1, 0)),
        ((0, 7), (0, 1)),
        ((2, 3), (2, 3)),
        ((6, 9), (2, 3)),
    ],
)
def test_vector_normalization(input, normalized):
    input_vector = Vector(*input).normalize()
    assert input_vector == Vector(*normalized)
    assert tuple(input_vector) == normalized
