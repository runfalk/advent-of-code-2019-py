from collections import defaultdict

from .common import last
from .intcode import Op
from .day5 import Interpreter as PrevInterpreter


class Interpreter(PrevInterpreter):
    def __init__(self, program):
        self.ptr = 0
        self.rel_base = 0
        self.program = defaultdict(int, enumerate(program))

    def set_rel_base(self, op):
        self.rel_base += self.read_input_param(op.modes[0])

    def step(self):
        op = super().step()
        if op is None:
            return
        elif op.code is Op.SET_REL_BASE:
            self.set_rel_base(op)
        else:
            return op


def solve(path):
    with open(path) as f:
        intcode = [int(byte) for byte in f.read().rstrip().split(",")]

    a = last(Interpreter.run_program(intcode, [1]))
    b = last(Interpreter.run_program(intcode, [2]))

    return (a, b)
