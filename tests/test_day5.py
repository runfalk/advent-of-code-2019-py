from aoc.day5 import Op, solve


def test_opcode():
    op = Op(11001)
    assert op.code == 1
    assert op.modes == [0, 1, 1]
    assert not op.is_by_val(0)
    assert op.is_by_val(1)
    assert op.is_by_val(2)


def test_solve():
    assert solve("data/day5.txt") == (8332629, 8805067)
