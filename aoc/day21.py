from .day9 import Interpreter
from .intcode import load_program_from_file


def springscript_compile(lines):
    for line in lines:
        for c in line:
            yield ord(c)
        yield ord("\n")


def springscript_run(intcode, lines):
    output = []
    for c in Interpreter.run_program(intcode, springscript_compile(lines)):
        if c >= 128:
            return c
        output.append(chr(c))
    raise RuntimeError("".join(output))


def solve(path):
    intcode = load_program_from_file(path)
    a = [
        # Jump if the square 1 blocks away is hole and 4 blocks away is ground
        "NOT A T",
        "AND D T",
        "OR T J",
        # Jump if the square 2 blocks away is hole and 4 blocks away is ground
        "NOT B T",
        "AND D T",
        "OR T J",
        # Jump if the square 3 blocks away is hole and 4 blocks away is ground
        "NOT C T",
        "AND D T",
        "OR T J",
        "WALK",
    ]

    # We can reuse the logic from A
    b = a[:-1] + [
        # Cancel the jump if we need to jump immediately again and would end up
        # in a hole
        "NOT J T",
        "AND J T",
        "OR E T",
        "OR H T",
        "AND T J",
        "RUN",
    ]

    return (springscript_run(intcode, a), springscript_run(intcode, b))
