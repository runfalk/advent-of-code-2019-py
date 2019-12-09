from .common import last
from .day5 import IntcodeInterpreter

def run(intcode, input=None):
    if input is None:
        input = []
    return IntcodeInterpreter(intcode).run(input)


def solve(path):
    with open(path) as f:
        intcode = [int(byte) for byte in f.read().rstrip().split(",")]

    a = last(run(intcode, [1]))
    b = last(run(intcode, [2]))

    return (a, b)
