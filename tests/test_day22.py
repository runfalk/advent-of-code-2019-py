import pytest

from aoc.day22 import get_target_pos, solve


@pytest.mark.parametrize(
    "instructions, num_cards, output",
    [
        (["deal into new stack",], 10, [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],),
        (["deal into new stack", "deal into new stack",], 10, list(range(10)),),
        (["deal with increment 7",], 10, [0, 3, 6, 9, 2, 5, 8, 1, 4, 7],),
        (["deal with increment 3",], 10, [0, 7, 4, 1, 8, 5, 2, 9, 6, 3],),
        (["cut 3",], 10, [3, 4, 5, 6, 7, 8, 9, 0, 1, 2],),
        (["cut -4",], 10, [6, 7, 8, 9, 0, 1, 2, 3, 4, 5],),
        (["cut -4", "deal into new stack",], 10, [5, 4, 3, 2, 1, 0, 9, 8, 7, 6],),
        (
            ["cut 6", "deal with increment 7", "deal into new stack",],
            10,
            [3, 0, 7, 4, 1, 8, 5, 2, 9, 6],
        ),
        (
            ["deal with increment 7", "deal with increment 9", "cut -2",],
            10,
            [6, 3, 0, 7, 4, 1, 8, 5, 2, 9],
        ),
        (
            [
                "deal into new stack",
                "cut -2",
                "deal with increment 7",
                "cut 8",
                "cut -4",
                "deal with increment 7",
                "cut 3",
                "deal with increment 9",
                "deal with increment 3",
                "cut -1",
            ],
            10,
            [9, 2, 5, 8, 1, 4, 7, 0, 3, 6],
        ),
        (
            [
                "deal with increment 7",
                "deal with increment 7",
                "deal with increment 9",
                "deal with increment 3",
            ],
            10,
            [0, 7, 4, 1, 8, 5, 2, 9, 6, 3],
        ),
        (["cut 1", "deal into new stack",], 3, [0, 2, 1],),
    ],
)
def test_apply_instructions(instructions, num_cards, output):
    result = [None] * num_cards
    for i in range(num_cards):
        new_pos = get_target_pos(instructions, num_cards, i)
        assert result[new_pos] is None
        result[new_pos] = i
    assert result == output


def test_solve():
    assert solve("data/day22.txt") == (1498, 74662303452927)
