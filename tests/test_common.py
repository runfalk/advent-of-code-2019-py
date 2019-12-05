import pytest

from aoc.common import Digits


@pytest.mark.parametrize(
    "value, base, output",
    [
        (123, 10, [3, 2, 1]),
        (0b1101, 2, [1, 0, 1, 1]),
        (0o123, 8, [3, 2, 1]),
        (0x123, 16, [3, 2, 1]),
    ],
)
def test_digits_iter(value, base, output):
    digits = Digits(value, base)
    assert list(digits) == output
    assert list(reversed(digits)) == list(reversed(output))
