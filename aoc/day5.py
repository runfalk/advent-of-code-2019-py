from collections import defaultdict

from .common import last
from .day2 import Interpreter as PrevInterpreter
from .intcode import Op


class Interpreter(PrevInterpreter):
    def jmp(self, op, jmp_if):
        comp = self.read_input_param(op.modes[0])
        jmp_target = self.read_input_param(op.modes[1])
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

    def step(self):
        op = super().step()

        if op is None:
            return
        elif op.code is Op.JMP_IF_TRUE:
            self.jmp(op, jmp_if=True)
        elif op.code is Op.JMP_IF_FALSE:
            self.jmp(op, jmp_if=False)
        elif op.code is Op.LT:
            self.lt(op)
        elif op.code is Op.EQ:
            self.eq(op)
        else:
            return op


def solve(path):
    with open(path) as f:
        intcode = [int(byte) for byte in f.read().rstrip().split(",")]

    a = last(Interpreter.run_program(intcode, [1]))
    b = last(Interpreter.run_program(intcode, [5]))

    return (a, b)
