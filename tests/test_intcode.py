from aoc.intcode import Mode, Op, Opcode


def test_opcode():
    op = Opcode(21001)
    assert op.code == Op.ADD
    assert op.modes[0] == Mode.POS
    assert op.modes[1] == Mode.IMMEDIATE
    assert op.modes[2] == Mode.RELATIVE
