import pytest

from aoc.day11 import solve


def test_solve():
    assert solve("data/day11.txt") == (
        2339,
        "\n".join(
            [
                "###   ##  #  # #### ###  #    ###  ### ",
                "#  # #  # #  # #    #  # #    #  # #  #",
                "#  # #    #  # ###  #  # #    #  # #  #",
                "###  # ## #  # #    ###  #    ###  ### ",
                "#    #  # #  # #    #    #    #    # # ",
                "#     ###  ##  #### #    #### #    #  #",
            ]
        ),
    )
