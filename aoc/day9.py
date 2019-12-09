from .common import last
from .day5 import intcode_eval


def solve(path):
    with open(path) as f:
        intcode = [int(byte) for byte in f.read().rstrip().split(",")]

    a = last(intcode_eval(intcode, [1]))
    b = last(intcode_eval(intcode, [2]))

    return (a, b)
