from aoc.day5 import Opcode, solve


def test_opcode():
    op = Opcode(11001)
    assert op.code == 1
    assert op.modes[0] == 0
    assert op.modes[1] == 1
    assert op.modes[2] == 1


def test_solve():
    assert solve("data/day5.txt") == (8332629, 8805067)
