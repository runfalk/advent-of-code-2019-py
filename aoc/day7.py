from collections import deque, namedtuple
from itertools import permutations

from .common import Digits, last
from .day5 import IntcodeInterpreter


def iter_deque(queue):
    while True:
        value = queue.popleft()
        if value is None:
            break
        yield value


def find_thruster_signal(intcode, phase_settings):
    interpreter = IntcodeInterpreter(intcode)

    prev_output = 0
    for phase in phase_settings:
        (prev_output,) = interpreter.run([phase, prev_output])

    return prev_output


def find_thruster_signal_with_feedback(intcode, phase_settings):
    a_input = deque([phase_settings[0], 0])
    b_input = deque([phase_settings[1]])
    c_input = deque([phase_settings[2]])
    d_input = deque([phase_settings[3]])
    e_input = deque([phase_settings[4]])

    a = IntcodeInterpreter(intcode).run(iter_deque(a_input))
    b = IntcodeInterpreter(intcode).run(iter_deque(b_input))
    c = IntcodeInterpreter(intcode).run(iter_deque(c_input))
    d = IntcodeInterpreter(intcode).run(iter_deque(d_input))
    e = IntcodeInterpreter(intcode).run(iter_deque(e_input))

    e_output = 0
    while True:
        b_input.append(next(a, None))
        c_input.append(next(b, None))
        d_input.append(next(c, None))
        e_input.append(next(d, None))

        try:
            e_output = next(e)
            a_input.append(e_output)
        except:
            break

    return e_output


def solve(path):
    with open(path) as f:
        intcode = [int(byte) for byte in f.read().rstrip().split(",")]

    a = max(
        find_thruster_signal(intcode, phase_settings)
        for phase_settings in permutations(range(5), r=5)
    )

    b = max(
        find_thruster_signal_with_feedback(intcode, phase_settings)
        for phase_settings in permutations(range(5, 10), r=5)
    )

    return (a, b)
