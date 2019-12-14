from collections import defaultdict

from .common import last
from .day2 import Interpreter as PrevInterpreter
from .intcode import load_program_from_file, Op


class Interpreter(PrevInterpreter):
    def __init__(self, program, op_overrides=None):
        ops = {
            Op.JMP_IF_TRUE: self.jmp,
            Op.JMP_IF_FALSE: self.jmp,
            Op.LT: self.lt,
            Op.EQ: self.eq,
        }

        if op_overrides is not None:
            ops.update(op_overrides.items())

        super().__init__(program, ops)

    def jmp(self, op):
        comp = self.read_input_param(op.modes[0])
        jmp_target = self.read_input_param(op.modes[1])
        jmp_if = op.code is Op.JMP_IF_TRUE
        if bool(comp) == jmp_if:
            self.ptr = jmp_target

    def lt(self, op):
        a = self.read_input_param(op.modes[0])
        b = self.read_input_param(op.modes[1])
        target = self.read_output_param(op.modes[2])
        self.program[target] = int(a < b)

    def eq(self, op):
        a = self.read_input_param(op.modes[0])
        b = self.read_input_param(op.modes[1])
        target = self.read_output_param(op.modes[2])
        self.program[target] = int(a == b)


def solve(path):
    intcode = load_program_from_file(path)
    a = last(Interpreter.run_program(intcode, [1]))
    b = last(Interpreter.run_program(intcode, [5]))

    return (a, b)
