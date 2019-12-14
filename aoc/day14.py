from collections import defaultdict

from .common import lines_from_file

# Number of available ores for part B
ORE_LIMIT = 1_000_000_000_000


def parse_reaction(s):
    def parse_pair(s):
        x, y = s.split(" ")
        return y, int(x)

    ingredients_str, output_str = s.split(" => ")
    name, min_quantity = parse_pair(output_str)
    return (
        name,
        (dict(map(parse_pair, ingredients_str.split(", "))), min_quantity),
    )


def divide_int_round_up(num, den):
    # Assumes positive numerator and denumerator
    return (num + den - 1) // den


def func_bisect_left(func, target_output, lower_bound=0):
    """
    Return the smallest integer input parameter for the given function that
    make the output value exceed the target value.

    This function works just like bisect.bisect_left but for functions.
    """

    upper_bound = lower_bound + 1

    # Establish an upper limit for the input value. We grow the value quickly
    # to get O(log n) performance
    while target_output > func(upper_bound):
        mid = (upper_bound - lower_bound) * 2 + 1
        lower_bound = upper_bound
        upper_bound += mid

    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        if func(mid) < target_output:
            lower_bound = mid + 1
        else:
            upper_bound = mid

    return lower_bound


def find_required_ores(reactions, num_fuel=1):
    stock = defaultdict(int)

    # Restock if necessary, then consume the given number of ingredients
    def restock_and_consume(ingredient, quantity):
        # We consider ore as always being available
        if ingredient == "ORE":
            stock["ORE"] -= quantity
            return

        components, min_quantity = reactions[ingredient]
        current_stock = stock[ingredient]

        if current_stock < quantity:
            # Find number of restocks to make
            num_restocks = divide_int_round_up(quantity - current_stock, min_quantity)

            # Only add the ingredients we don't immediately consume to stock
            stock[ingredient] += num_restocks * min_quantity - quantity

            # Ensure that all children's stock are taken into account
            for cname, cquantity in components.items():
                restock_and_consume(cname, num_restocks * cquantity)
        else:
            # We only need to consume since the resources we needed were in
            # stock
            stock[ingredient] -= quantity

    restock_and_consume("FUEL", num_fuel)
    return abs(stock["ORE"])


def find_max_fuel(reactions, num_ores):
    return (
        func_bisect_left(
            lambda num_fuel: find_required_ores(reactions, num_fuel), ORE_LIMIT,
        )
        - 1
    )


def solve(path):
    reactions = dict(map(parse_reaction, lines_from_file(path)))
    return (
        find_required_ores(reactions),
        find_max_fuel(reactions, ORE_LIMIT),
    )
