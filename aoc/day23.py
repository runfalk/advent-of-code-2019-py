import asyncio

from .day9 import Interpreter
from .intcode import load_program_from_file, Op


async def run_computer(program, addr, input_queue, output_queue):
    computer = Interpreter(program)
    it = computer.step_until_halt()

    # Get address from queue
    op = next(it)
    assert op.code == Op.INPUT
    target = computer.read_output_param(op.modes[0])
    computer.program[target] = addr

    while op := next(it, None):
        # Allow other computers to run in the event loop
        await asyncio.sleep(0)

        if op.code == Op.INPUT:
            target = computer.read_output_param(op.modes[0])

            try:
                x, y = input_queue.get_nowait()
                computer.program[target] = x

                op = next(it)
                assert op.code == Op.INPUT
                target = computer.read_output_param(op.modes[0])

                computer.program[target] = y
            except asyncio.QueueEmpty:
                computer.program[target] = -1
        elif op.code == Op.OUTPUT:
            target = computer.read_input_param(op.modes[0])

            op = next(it)
            assert op.code == Op.OUTPUT
            x = computer.read_input_param(op.modes[0])

            op = next(it)
            assert op.code == Op.OUTPUT
            y = computer.read_input_param(op.modes[0])

            await output_queue.put((target, x, y))
        else:
            raise ValueError(f"Unexpected OP-code {op!r}")


async def router(input_queue, computers):
    first_nat_y = None
    prev_nat_x, prev_nat_y = None, None
    computer_zero_nat_y_history = set()

    while True:
        try:
            addr, x, y = await asyncio.wait_for(input_queue.get(), timeout=0.05)
        except asyncio.TimeoutError:
            # Network acivity has stagnated. Determine if we need to revive the
            # network using a NAT package
            if prev_nat_y in computer_zero_nat_y_history:
                return first_nat_y, prev_nat_y
            computer_zero_nat_y_history.add(prev_nat_y)
            addr, x, y = 0, prev_nat_x, prev_nat_y

        if addr == 255:
            prev_nat_x, prev_nat_y = x, y
            if first_nat_y is None:
                first_nat_y = prev_nat_y
        else:
            await computers[addr].put((x, y))


async def run(intcode):
    output_queue = asyncio.Queue()
    input_queues = [asyncio.Queue() for addr in range(50)]

    computer_tasks = [
        asyncio.create_task(run_computer(intcode, addr, q, output_queue))
        for addr, q in enumerate(input_queues)
    ]

    first_nat_y, first_repeated_y = await router(output_queue, input_queues)

    for ct in computer_tasks:
        await Interpreter.shutdown_async_program(ct)

    return first_nat_y, first_repeated_y


def solve(path):
    intcode = load_program_from_file(path)
    return asyncio.run(run(intcode))
