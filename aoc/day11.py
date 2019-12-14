from collections import defaultdict

from .common import coords_as_str
from .intcode import load_program_from_file
from .plane import Coord
from .day8 import iter_chunks
from .day9 import Interpreter


class Robot:
    def __init__(self):
        self.position = Coord(0, 0)
        self.direction = "U"
        self.tiles = defaultdict(int)

    def _current_color(self):
        while True:
            yield self.tiles[self.position]

    def rotate_cw(self):
        self.direction = {"U": "R", "R": "D", "D": "L", "L": "U",}[self.direction]

    def rotate_ccw(self):
        self.rotate_cw()
        self.rotate_cw()
        self.rotate_cw()

    def advance(self):
        self.position = {
            "U": self.position.up,
            "R": self.position.right,
            "D": self.position.down,
            "L": self.position.left,
        }[self.direction](1)

    def run(self, intcode):
        program_output = Interpreter.run_program(intcode, self._current_color())
        for color, rotation in iter_chunks(2, program_output):
            if color not in (0, 1):
                raise ValueError(f"Unexpected color ({color})")
            self.tiles[self.position] = color

            if rotation == 0:
                self.rotate_ccw()
            elif rotation == 1:
                self.rotate_cw()
            else:
                raise ValueError(f"Unexpected rotation direction ({rotation})")

            self.advance()


def start_on_black(intcode):
    robot = Robot()
    robot.run(intcode)
    return robot.tiles


def start_on_white(intcode):
    robot = Robot()
    robot.tiles[robot.position] = 1
    robot.run(intcode)
    return robot.tiles


def solve(path):
    intcode = load_program_from_file(path)
    return (
        len(start_on_black(intcode)),
        coords_as_str(
            coord for coord, color in start_on_white(intcode).items() if color == 1
        ),
    )
