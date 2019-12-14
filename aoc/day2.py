from .intcode import InterpreterBase, load_program_from_file, Op


class Interpreter(InterpreterBase):
    def __init__(self, program, op_overrides=None):
        ops = {
            Op.ADD: self.add,
            Op.MUL: self.mul,
        }

        if op_overrides is not None:
            ops.update(op_overrides.items())

        super().__init__(program, ops)

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


def run_program(program, noun=None, verb=None):
    program = list(program)

    if noun is not None:
        program[1] = noun
    if verb is not None:
        program[2] = verb

    computer = Interpreter(program)
    for op in computer.step_until_halt():
        raise ValueError(f"Unknown opcode {op!r}")
    return computer.program


def find_noun_and_verb(program):
    for noun in range(100):
        for verb in range(100):
            b = run_program(program, noun, verb)

            if b[0] == 19690720:
                return 100 * noun + verb


def solve(path):
    intcode = load_program_from_file(path)
    a = run_program(intcode, noun=12, verb=2)
    b = find_noun_and_verb(intcode)

    return (a[0], b)
