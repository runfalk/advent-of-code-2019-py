from collections import namedtuple

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


class Op:
    __slots__ = "_code"

    def __init__(self, code):
        self._code = code

    def __repr__(self):
        return "Op(code={}, modes={})".format(self.code, self.modes)

    @property
    def code(self):
        return self._code % 100

    @property
    def modes(self):
        return list(Digits(self._code))[2:]

    def is_by_val(self, i):
        return Digits(self._code)[i + 2]


class IntcodeInterpreter:
    def __init__(self, program):
        self.ptr = 0
        self.rel_base = 0
        self.program = {i: b for i, b in enumerate(program)}

    def _peek(self, method=1):
        if method == 0:
            pos = self.program.get(self.ptr, 0)
        elif method == 1:
            pos = self.ptr
        elif method == 2:
            pos = self.program.get(self.ptr, 0) + self.rel_base
        else:
            raise ValueError("Method must be 0, 1 or 2, got {}".format(method))

        if pos < 0:
            raise IndexError("Tried to read outside of memory")
        return self.program.get(pos, 0)

    def _read(self, method=1):
        value = self._peek(method)
        self.ptr += 1
        return value

    def _write(self, method, key, value):
        if method == 0:
            self.program[key] = value
        elif method == 1:
            raise ValueError("Can't write output to parameter in immediate mode")
        elif method == 2:
            self.program[self.rel_base + key] = value

    def add(self, op):
        a = self._read(op.is_by_val(0))
        b = self._read(op.is_by_val(1))
        target = self._read()
        self._write(op.is_by_val(2), target, a + b)
        self.program[target] = a + b

    def mul(self, op):
        a = self._read(op.is_by_val(0))
        b = self._read(op.is_by_val(1))
        target = self._read()
        self._write(op.is_by_val(2), target, a * b)

    def jmp(self, op, cond):
        comp = self._read(op.is_by_val(0))
        jmp_target = self._read(op.is_by_val(1))
        if bool(comp) == cond:
            self.ptr = jmp_target

    def lt(self, op):
        a = self._read(op.is_by_val(0))
        b = self._read(op.is_by_val(1))
        target = self._read()

        if a < b:
            self._write(op.is_by_val(2), target, 1)
        else:
            self._write(op.is_by_val(2), target, 0)

    def eq(self, op):
        a = self._read(op.is_by_val(0))
        b = self._read(op.is_by_val(1))
        target = self._read()

        if a == b:
            self._write(op.is_by_val(2), target, 1)
        else:
            self._write(op.is_by_val(2), target, 0)

    def run(self, input):
        """Returns a generator that yields on every output instruction"""
        # Each time an input opcode is reached a value from this iterator i consumed
        input_iter = iter(input)

        # Save the untouched program in order to restore it after execution
        saved_program = dict(self.program.items())

        try:
            while True:
                op = Op(self._read())

                if op.code == OP_ADD:
                    self.add(op)
                elif op.code == OP_MUL:
                    self.mul(op)
                elif op.code == OP_INPUT:
                    self._write(op.is_by_val(0), self._read(), next(input_iter))
                elif op.code == OP_OUTPUT:
                    yield self._read(op.is_by_val(0))
                elif op.code == OP_JMP_IF_TRUE:
                    self.jmp(op, cond=True)
                elif op.code == OP_JMP_IF_FALSE:
                    self.jmp(op, cond=False)
                elif op.code == OP_LT:
                    self.lt(op)
                elif op.code == OP_EQ:
                    self.eq(op)
                elif op.code == OP_SET_REL_BASE:
                    self.rel_base += self._read(op.is_by_val(0))
                elif op.code == OP_EXIT:
                    break
                else:
                    raise ValueError("Unexpected OP-code {!r}".format(op))
        finally:
            self.ptr = 0
            self.rel_base = 0
            self.program = saved_program


def solve(path):
    with open(path) as f:
        intcode = [int(byte) for byte in f.read().rstrip().split(",")]

    interpreter = IntcodeInterpreter(intcode)

    a = last(interpreter.run([1]))
    b = last(interpreter.run([5]))

    return (a, b)
