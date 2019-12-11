from collections import defaultdict
from enum import Enum, IntEnum

from .common import Digits


class Mode(Enum):
    POS = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Op(IntEnum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JMP_IF_TRUE = 5
    JMP_IF_FALSE = 6
    LT = 7
    EQ = 8
    SET_REL_BASE = 9
    EXIT = 99


class Opcode:
    __slots__ = "_code"

    def __init__(self, code):
        self._code = code

    def __repr__(self):
        return f"Opcode(code={self.code!r}, modes={dict(self.modes.items())})"

    @property
    def code(self):
        return Op(self._code % 100)

    @property
    def modes(self):
        modes = defaultdict(lambda: Mode.POS)
        for i, mode in enumerate(Digits(self._code // 100)):
            modes[i] = Mode(mode)
        return modes


class InterpreterBase:
    def __init__(self, program):
        self.ptr = 0
        self.rel_base = 0
        self.program = list(program)

    @classmethod
    def run_program(cls, program, input=None):
        """Run program with iterator based input and output"""
        input_iter = iter([] if input is None else input)
        computer = cls(program)
        for op in computer.step_until_halt():
            if op.code == Op.INPUT:
                target = computer.read_output_param(op.modes[0])
                computer.program[target] = next(input_iter)
            elif op.code == Op.OUTPUT:
                yield computer.read_input_param(op.modes[0])
            else:
                raise ValueError(f"Unexpected OP-code {op!r}")

    def read_opcode(self):
        return Opcode(self.read_input_param(Mode.IMMEDIATE))

    def read_input_param(self, mode):
        if mode == Mode.POS:
            pos = self.program[self.ptr]
        elif mode == Mode.IMMEDIATE:
            pos = self.ptr
        elif mode == Mode.RELATIVE:
            pos = self.program[self.ptr] + self.rel_base
        else:
            raise ValueError("Mode must be got {!r}".format(mode))

        if pos < 0:
            raise IndexError("Tried to read outside of memory")

        self.ptr += 1
        return self.program[pos]

    def read_output_param(self, mode):
        if mode == Mode.POS:
            pos = self.program[self.ptr]
        elif mode == Mode.IMMEDIATE:
            raise ValueError("Output parameters can't be immediate")
        elif mode == Mode.RELATIVE:
            pos = self.program[self.ptr] + self.rel_base
        else:
            raise ValueError(
                "Output parameter mode must be 0 or 2, got {}".format(mode)
            )

        if pos < 0:
            raise IndexError("Tried to read outside of memory")

        self.ptr += 1
        return pos

    def step(self):
        return self.read_opcode()

    def step_until_halt(self):
        while True:
            op = self.step()
            if op is None:
                continue
            if op.code is Op.EXIT:
                return
            else:
                yield op
