from collections import defaultdict

from .common import last
from .intcode import load_program_from_file, Op
from .day5 import Interpreter as PrevInterpreter


class Interpreter(PrevInterpreter):
    def __init__(self, program, op_overrides=None):
        ops = {
            Op.SET_REL_BASE: self.set_rel_base,
        }

        if op_overrides is not None:
            ops.update(op_overrides.items())

        # We don't send the real program to the parent since we will override
        # it with a defaultdict anyway. This is required since the memory is
        # unbounded
        super().__init__([], ops)
        self.program = defaultdict(int, enumerate(program))

    def set_rel_base(self, op):
        self.rel_base += self.read_input_param(op.modes[0])


def solve(path):
    intcode = load_program_from_file(path)
    a = last(Interpreter.run_program(intcode, [1]))
    b = last(Interpreter.run_program(intcode, [2]))

    return (a, b)
