OP_ADD = 1
OP_MUL = 2
OP_EXIT = 99


def run_program(program, noun=None, verb=None):
    program = list(program)

    if noun is not None:
        program[1] = noun
    if verb is not None:
        program[2] = verb

    i = 0
    while program[i] != 99:
        op = program[i]
        if op == OP_ADD:
            program[program[i + 3]] = program[program[i + 1]] + program[program[i + 2]]
        elif op == OP_MUL:
            program[program[i + 3]] = program[program[i + 1]] * program[program[i + 2]]
        else:
            raise ValueError("Unexpected OP-code")

        # All instructions are four wide
        i += 4

    return program


def find_noun_and_verb(program):
    for noun in range(100):
        for verb in range(100):
            b = run_program(program, noun, verb)

            if b[0] == 19690720:
                return 100 * noun + verb


def solve(path):
    with open(path) as f:
        intcode = [int(byte) for byte in f.read().rstrip().split(",")]

    a = run_program(intcode, noun=12, verb=2)
    b = find_noun_and_verb(intcode)

    return (a[0], b)
