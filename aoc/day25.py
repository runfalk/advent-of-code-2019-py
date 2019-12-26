from click import getchar
from collections import deque

from .day9 import Interpreter
from .intcode import load_program_from_file, Op


def get_selection(items):
    sorted_items = sorted(items)
    if len(sorted_items) == 1:
        return sorted_items[0]

    print(
        "Select item:",
        ", ".join(f"{i} {name}" for i, name in enumerate(sorted_items, 1)),
    )
    try:
        return sorted_items[int(getchar()) - 1]
    except (ValueError, IndexError):
        pass


def get_action(doors, inv_items, tile_items):
    c = getchar()
    if c == "\x1b[A" and "north" in doors:
        return "north"
    elif c == "\x1b[C" and "east" in doors:
        return "east"
    elif c == "\x1b[B" and "south" in doors:
        return "south"
    elif c == "\x1b[D" and "west" in doors:
        return "west"
    elif c == "t" and tile_items:
        item = get_selection(tile_items)
        if item is None:
            print("Invalid selection")
        else:
            return f"take {item}"
    elif c == "d" and inv_items:
        item = get_selection(inv_items)
        if item is None:
            print("Invalid selection")
        else:
            return f"drop {item}"
    elif c == " ":
        print()
        return input("Input command: ")
    return get_action(doors, inv_items, tile_items)


def run(intcode):
    computer = Interpreter(intcode)

    lines = []
    line = []

    inputs = deque()
    doors = set()
    inv_items = set()
    tile_items = set()
    for op in computer.step_until_halt():
        if op.code == Op.INPUT:
            # If we don't have any input we must ask for a command
            if not inputs:
                # Extract information from the current room
                for i, l in enumerate(lines):
                    if l == "Doors here lead:":
                        doors.clear()
                        doors_start = i + 1
                        doors_end = doors_start
                        while lines[doors_end].startswith("-"):
                            doors_end += 1

                        for door in lines[doors_start:doors_end]:
                            doors.add(door[2:])
                    elif l == "Items here:":
                        tile_items.clear()
                        items_start = i + 1
                        items_end = items_start
                        while lines[items_end].startswith("-"):
                            items_end += 1

                        for item in lines[items_start:items_end]:
                            tile_items.add(item[2:])
                    elif l.startswith("You take the"):
                        item = l[13:-1]
                        inv_items.add(item)
                        tile_items.remove(item)
                    elif l.startswith("You drop the"):
                        item = l[13:-1]
                        tile_items.add(item)
                        inv_items.remove(item)

                if lines:
                    for l in lines:
                        if l == "Command?":
                            break
                        print(l)

                    inv_items_str = ", ".join(sorted(inv_items))
                    if not inv_items_str:
                        inv_items_str = "<empty>"
                    print("Inventory:", inv_items_str)
                    lines = []

                cmd = get_action(doors, inv_items, tile_items)
                inputs.extend(map(ord, cmd))
                inputs.append(ord("\n"))

            target = computer.read_output_param(op.modes[0])
            computer.program[target] = inputs.popleft()
        elif op.code == Op.OUTPUT:
            char = chr(computer.read_input_param(op.modes[0]))
            if char == "\n":
                lines.append("".join(line))
                line = []
            else:
                line.append(char)

    if line:
        lines.append("".join(line))
    print("\n".join(lines))


def solve(path):
    # My solution's items: astrolabe, food ration, ornament and weather machine
    intcode = load_program_from_file(path)
    run(intcode)
    exit(0)
