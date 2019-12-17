from collections import Counter
from itertools import combinations

from .common import last
from .day9 import Interpreter
from .intcode import load_program_from_file
from .plane import Coord


def join_moves(items):
    return ",".join(str(d) for d in items)


def iter_intersections(scaffolds):
    for coord in scaffolds:
        if all(n in scaffolds for n in coord.iter_neighbors()):
            yield coord


class Cleaner:
    def __init__(self, start, direction):
        self.pos = start
        self.dir = direction

    def next_pos(self):
        dir_to_pos = {
            0: self.pos.up,
            1: self.pos.right,
            2: self.pos.down,
            3: self.pos.left,
        }
        return dir_to_pos[self.dir]()

    def turn_left(self):
        self.dir = (self.dir - 1) % 4

    def turn_right(self):
        self.dir = (self.dir + 1) % 4

    def advance(self):
        next_pos = self.next_pos()
        self.pos = next_pos
        return self.pos


def follow_scaffolding(robot, scaffolds):
    curr_steps = 0
    while True:
        next_pos = robot.next_pos()
        if next_pos not in scaffolds:
            if curr_steps:
                yield curr_steps
            curr_steps = 0

            robot.turn_right()
            if robot.next_pos() in scaffolds:
                yield "R"
                continue

            robot.turn_left()
            robot.turn_left()
            if robot.next_pos() in scaffolds:
                yield "L"
                continue

            # We have reached the end
            break

        robot.advance()
        curr_steps += 1


def iter_patterns(l, min_len=2):
    l_len = len(l)
    for start in range(l_len - min_len + 1):
        for end in range(start + min_len, l_len + 1):
            yield tuple(l[start:end])


def compile_routines(moves):
    max_subroutine_len = 20

    # Store patterns using a set to avoid duplicates. Skip too long patterns
    patterns = {
        p for p in iter_patterns(moves) if len(join_moves(p)) <= max_subroutine_len
    }

    # Count the number of times each pattern occurs
    occurences = Counter()
    for p in patterns:
        for start in range(len(moves) - len(p) + 1):
            if moves[start : start + len(p)] == list(p):
                occurences[p] += 1

    # Without sorting the speed varies greatly between runs since set order is
    # determined by startup seed
    def pattern_score(p):
        # A pattern is scored by the number of characters it saves per use
        # times the number of times it occurs in the move list
        return (len(join_moves(p)) - 1) * occurences[p]

    subroutines = list(patterns)
    subroutines.sort(key=pattern_score, reverse=True)

    for selection in combinations(subroutines, 3):
        main_program = use_subroutines(moves, selection)
        if main_program is None:
            continue

        if len(join_moves(main_program)) <= max_subroutine_len:
            return [
                tuple(main_program),
                selection[0],
                selection[1],
                selection[2],
            ]
    raise ValueError("No way to make valid subroutines for this input")


def use_subroutines(moves, patterns):
    # We sort this to always try the longest subroutine first
    by_len = lambda x: len(x[1])
    subroutines = list(sorted(zip(["A", "B", "C"], patterns), key=by_len, reverse=True))

    i = 0
    main_routine = []
    while i < len(moves):
        for name, pattern in subroutines:
            if moves[i : i + len(pattern)] == list(pattern):
                main_routine.append(name)
                i += len(pattern)
                break
        else:
            # This means we weren't able to use any subroutine for this move and
            # the subroutine combination is not the correct answer
            return
    return main_routine


def extract_scaffolding(intcode):
    robot_chars = ["^", ">", "v", "<"]

    x = 0
    y = 0
    robot = None
    scaffolds = set()
    for char in Interpreter.run_program(intcode):
        char = chr(char)
        if char == "\n":
            y += 1
            x = 0
            continue

        coord = Coord(x, y)
        if char in robot_chars:
            robot = Cleaner(coord, direction=robot_chars.index(char))
        elif char == "#":
            scaffolds.add(coord)
        x += 1
    return scaffolds, robot


def solve(path):
    intcode = load_program_from_file(path)

    scaffolds, robot = extract_scaffolding(intcode)
    a = sum(c.x * c.y for c in iter_intersections(scaffolds))

    moves = list(follow_scaffolding(robot, scaffolds))
    movement_routines = compile_routines(moves)

    # Don't debug print ("y" to enable)
    movement_routines.append("n")

    # Put computer in run mode
    intcode[0] = 2

    ascii_input = "\n".join(map(join_moves, movement_routines)) + "\n"
    print(ascii_input)
    b = last(Interpreter.run_program(intcode, list(map(ord, ascii_input))))
    return (a, b)
