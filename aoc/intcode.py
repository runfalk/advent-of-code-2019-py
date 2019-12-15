import asyncio

from enum import Enum, IntEnum
from itertools import count


class Mode:
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


class ModeDict(dict):
    __slots__ = ()

    def __missing__(self, key):
        return 0


class Opcode:
    __slots__ = ("code", "modes")

    def __init__(self, code):
        self.code = Op(code % 100)

        modes = ModeDict()
        int_modes = code // 100
        for i in count():
            if int_modes == 0:
                break
            modes[i] = int_modes % 10
            int_modes //= 10
        self.modes = modes

    def __repr__(self):
        return f"Opcode(code={self.code!r}, modes={self.modes.items()})"


class InterpreterBase:
    def __init__(self, program, op_overrides=None):
        self.ptr = 0
        self.rel_base = 0
        self.program = list(program)
        self.ops = {}
        if op_overrides is not None:
            self.ops.update(op_overrides.items())

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

    @classmethod
    async def async_run_program(cls, program, input_queue, output_queue):
        computer = cls(program)
        for op in computer.step_until_halt():
            if op.code == Op.INPUT:
                target = computer.read_output_param(op.modes[0])
                computer.program[target] = await input_queue.get()
            elif op.code == Op.OUTPUT:
                await output_queue.put(computer.read_input_param(op.modes[0]))
            else:
                raise ValueError(f"Unexpected OP-code {op!r}")

    @staticmethod
    async def shutdown_async_program(task):
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

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

    def step_until_halt(self):
        while True:
            op = self.read_opcode()
            func = self.ops.get(op.code)

            if op.code is Op.EXIT:
                return
            elif func is not None:
                func(op)
            else:
                yield op


def load_program_from_file(path):
    with open(path) as f:
        return [int(byte) for byte in f.read().rstrip().split(",")]
