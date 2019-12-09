from collections import defaultdict

from .common import Digits, last


OP_ADD = 1
OP_MUL = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JMP_IF_TRUE = 5
OP_JMP_IF_FALSE = 6
OP_LT = 7
OP_EQ = 8
OP_SET_REL_BASE = 9
OP_EXIT = 99

MODE_POS = 0
MODE_IMMEDIATE = 1
MODE_RELATIVE = 2


class Opcode:
    __slots__ = "_code"

    def __init__(self, code):
        self._code = code

    def __repr__(self):
        return "Opcode(code={}, modes={})".format(self.code, self.modes)

    @property
    def code(self):
        return self._code % 100

    @property
    def modes(self):
        return Digits(self._code // 100)


class Interpreter:
    def __init__(self, program):
        self.ptr = 0
        self.rel_base = 0
        self.program = defaultdict(int, enumerate(program))

    def read_opcode(self):
        return Opcode(self.read_input_param(MODE_IMMEDIATE))

    def read_input_param(self, mode):
        if mode == MODE_POS:
            pos = self.program[self.ptr]
        elif mode == MODE_IMMEDIATE:
            pos = self.ptr
        elif mode == MODE_RELATIVE:
            pos = self.program[self.ptr] + self.rel_base
        else:
            raise ValueError("Mode must be 0, 1 or 2, got {}".format(mode))

        if pos < 0:
            raise IndexError("Tried to read outside of memory")

        self.ptr += 1
        return self.program[pos]

    def read_output_param(self, mode):
        if mode == MODE_POS:
            pos = self.program[self.ptr]
        elif mode == MODE_IMMEDIATE:
            raise ValueError("Output parameters can't be immediate")
        elif mode == MODE_RELATIVE:
            pos = self.program[self.ptr] + self.rel_base
        else:
            raise ValueError(
                "Output parameter mode must be 0 or 2, got {}".format(mode)
            )

        if pos < 0:
            raise IndexError("Tried to read outside of memory")

        self.ptr += 1
        return pos

    def add(self, op):
        a = self.read_input_param(op.modes[0])
        b = self.read_input_param(op.modes[1])
        target = self.read_output_param(op.modes[2])
        self.program[target] = a + b

    def mul(self, op):
        a = self.read_input_param(op.modes[0])
        b = self.read_input_param(op.modes[1])
        target = self.read_output_param(op.modes[2])
        self.program[target] = a * b

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

    def set_rel_base(self, op):
        self.rel_base += self.read_input_param(op.modes[0])


def intcode_eval(program, input):
    """Returns a generator that yields on every output instruction"""
    # Each time an input opcode is reached a value from this iterator i consumed
    input_iter = iter(input)

    vm = Interpreter(program)
    while True:
        op = vm.read_opcode()

        if op.code == OP_ADD:
            vm.add(op)
        elif op.code == OP_MUL:
            vm.mul(op)
        elif op.code == OP_INPUT:
            vm.program[vm.read_output_param(op.modes[0])] = next(input_iter)
        elif op.code == OP_OUTPUT:
            yield vm.read_input_param(op.modes[0])
        elif op.code == OP_JMP_IF_TRUE:
            vm.jmp(op, jmp_if=True)
        elif op.code == OP_JMP_IF_FALSE:
            vm.jmp(op, jmp_if=False)
        elif op.code == OP_LT:
            vm.lt(op)
        elif op.code == OP_EQ:
            vm.eq(op)
        elif op.code == OP_SET_REL_BASE:
            vm.set_rel_base(op)
        elif op.code == OP_EXIT:
            break
        else:
            raise ValueError("Unexpected OP-code {!r}".format(op))


def solve(path):
    with open(path) as f:
        intcode = [int(byte) for byte in f.read().rstrip().split(",")]

    a = last(intcode_eval(intcode, [1]))
    b = last(intcode_eval(intcode, [5]))

    return (a, b)
