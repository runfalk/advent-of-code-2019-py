import asyncio

from collections import deque
from itertools import cycle, islice, permutations

from .day5 import Interpreter, Op


def find_thruster_signal(intcode, phase_settings):
    prev_output = 0
    for phase in phase_settings:
        (prev_output,) = Interpreter.run_program(intcode, [phase, prev_output])
    return prev_output


def async_queue_from_iter(it):
    queue = asyncio.Queue()
    for item in it:
        queue.put_nowait(item)
    return queue


async def async_run_program(program, input_queue, output_queue):
    computer = Interpreter(program)
    for op in computer.step_until_halt():
        if op.code == Op.INPUT:
            target = computer.read_output_param(op.modes[0])
            computer.program[target] = await input_queue.get()
        elif op.code == Op.OUTPUT:
            await output_queue.put(computer.read_input_param(op.modes[0]))
        else:
            raise ValueError(f"Unexpected OP-code {op!r}")


async def find_thruster_signal_with_feedback(intcode, phase_settings):
    input_queues = [
        async_queue_from_iter([phase_setting]) for phase_setting in phase_settings
    ]

    # Add initial zero to first amplifier's queue
    await input_queues[0].put(0)

    # Start amplifier programs and hook them up to the correct IO
    output_queue_iter = islice(cycle(input_queues), 1, None)
    amplifiers = [
        async_run_program(intcode, input_queue, output_queue)
        for input_queue, output_queue in zip(input_queues, output_queue_iter)
    ]

    await asyncio.gather(*amplifiers)

    # There should be one item in the first amplifier's queue waiting for us
    return await input_queues[0].get()


def solve(path):
    with open(path) as f:
        intcode = [int(byte) for byte in f.read().rstrip().split(",")]

    a = max(
        find_thruster_signal(intcode, phase_settings)
        for phase_settings in permutations(range(5))
    )

    b = max(
        asyncio.run(find_thruster_signal_with_feedback(intcode, phase_settings))
        for phase_settings in permutations(range(5, 10))
    )

    return (a, b)
