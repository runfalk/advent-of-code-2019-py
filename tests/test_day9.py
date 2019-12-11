import pytest

from aoc.day9 import Interpreter, solve


# fmt: off
@pytest.mark.parametrize("program, output", [
    (
        [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],
        [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],
    ),
    (
        [1102,34915192,34915192,7,4,7,99,0],
        [1219070632396864],
    ),
    (
        [104,1125899906842624,99],
        [1125899906842624],
    ),
])
# fmt: on
def test_intcode_eval(program, output):
    assert list(Interpreter.run_program(program, [])) == output


def test_solve():
    assert solve("data/day9.txt") == (3100786347, 87023)
