from aoc.common import lines_from_file


def instructions_to_polynomial(instructions, num_cards):
    # Construct a polynomial from the instructions. Since all techniques can be
    # expressed using linear equations we can combine them to a single linear
    # equation y = kx + m mod n, where:
    # - y is the new position after shuffling
    # - x is a card's initial position
    # - n is the number of cards
    k = 1
    m = 0

    for instruction in instructions:
        if instruction == "deal into new stack":
            k *= -1
            m = num_cards - m - 1
        elif instruction.startswith("deal with increment"):
            step = int(instruction[instruction.rindex(" ") + 1 :])
            k *= step
            m *= step
        elif instruction.startswith("cut"):
            step = int(instruction[instruction.rindex(" ") + 1 :])
            m -= step
        else:
            raise ValueError(f"Unknown instruction {instruction!r}")
        k %= num_cards
        m %= num_cards
    return k, m


def lcg_step(k, m, n, x, steps=1):
    # This is a special case since we'd divide by zero otherwise
    if steps == 1:
        return (k * x + m) % n

    # Special handling
    if steps < 0:
        k_inv = pow(k, -1, n)
        k = k_inv
        m = m * -k_inv
        steps = abs(steps)

    m = (pow(k, steps, (k - 1) * n) - 1) // (k - 1) * m
    k = pow(k, steps, n)
    return (k * x + m) % n


def get_target_pos(instructions, num_cards, pos, num_shuffles=1):
    k, m = instructions_to_polynomial(instructions, num_cards)

    # The expression kx + m mod n is something called a linear congruent
    # generator and is useful as a pseudo-random number generator. Since this is
    # a well explored concept there are great ways of stepping this generator
    # both backwards and forwards
    return lcg_step(k, m, n=num_cards, x=pos, steps=num_shuffles)


def solve(path):
    instructions = list(lines_from_file(path))
    return (
        get_target_pos(instructions, num_cards=10_007, pos=2019),
        get_target_pos(
            instructions,
            num_cards=119_315_717_514_047,
            pos=2020,
            num_shuffles=-101_741_582_076_661,
        ),
    )
