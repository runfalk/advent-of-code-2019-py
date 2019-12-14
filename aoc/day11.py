from collections import defaultdict

from .common import coords_as_str
from .intcode import load_program_from_file
from .plane import Coord
from .day8 import iter_chunks
from .day9 import Interpreter


class Robot:
    def __init__(self, tiles=None):
        self.position = Coord(0, 0)
        self.direction = "U"
        self.tiles = defaultdict(int)

        if tiles is not None:
            self.tiles.update(tiles.items())

    def current_color(self):
        return self.tiles[self.position]

    def rotate_cw(self):
        self.direction = {"U": "R", "R": "D", "D": "L", "L": "U"}[self.direction]

    def rotate_ccw(self):
        self.direction = {"U": "L", "R": "U", "D": "R", "L": "D"}[self.direction]

    def advance(self):
        self.position = {
            "U": self.position.up,
            "R": self.position.right,
            "D": self.position.down,
            "L": self.position.left,
        }[self.direction]()


def run_robot(intcode, tiles=None):
    robot = Robot(tiles)

    def iter_current_color():
        while True:
            yield robot.current_color()

    program_output = Interpreter.run_program(intcode, iter_current_color())
    for color, rotation in iter_chunks(2, program_output):
        if color not in (0, 1):
            raise ValueError(f"Unexpected color ({color})")
        robot.tiles[robot.position] = color

        if rotation == 0:
            robot.rotate_ccw()
        elif rotation == 1:
            robot.rotate_cw()
        else:
            raise ValueError(f"Unexpected rotation direction ({rotation})")

        robot.advance()
    return robot.tiles


def start_on_white(intcode):
    robot = Robot()
    robot.tiles[robot.position] = 1
    robot.run(intcode)
    return robot.tiles


def solve(path):
    intcode = load_program_from_file(path)
    b = run_robot(intcode, tiles={Coord(0, 0): 1})
    return (
        len(run_robot(intcode)),
        coords_as_str(coord for coord, color in b.items() if color == 1),
    )
