from collections import Counter

from .common import dict_coords_as_str
from .day12 import cmp
from .day8 import iter_chunks
from .day9 import Interpreter
from .intcode import load_program_from_file
from .plane import Coord


def find_num_blocks(intcode):
    computer = Interpreter.run_program(intcode)
    tiles = Counter(tile_id for _, _, tile_id in iter_chunks(3, computer))

    return tiles[Bot.BLOCK]


class Bot:
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    def __init__(self, intcode, debug=False):
        intcode = list(intcode)

        # Put the game in free to play mode
        intcode[0] = 2

        # Frame buffer
        self.fb = {}

        # Metadata to decide joystick input
        self.computer = Interpreter.run_program(intcode, self.input())
        self.paddle = Coord(0, 0)
        self.ball = Coord(0, 0)
        self.ball_delta = None

        self.score = 0
        self.debug = debug

    def input(self):
        while True:
            # We need to reset the delta when the ball hits the paddle since it
            # bounces back in the same direction it came from
            is_paddle_hit = self.paddle.up() == self.ball
            if is_paddle_hit:
                self.ball_delta = Coord(0, 0)

            paddle_dx = self.paddle.x - (self.ball.x + self.ball_delta.x)

            if self.debug:
                print(
                    dict_coords_as_str(
                        self.fb,
                        {
                            self.EMPTY: " ",
                            self.WALL: "#",
                            self.BLOCK: "X",
                            self.PADDLE: "_",
                            self.BALL: "o",
                        },
                    )
                )
                print("Paddle:", self.paddle)
                print("Ball:", self.ball, self.ball_delta)
                print("Move:", cmp(0, paddle_dx))
                print("Score:", self.score)

            yield cmp(0, paddle_dx)

    def run_segment(self):
        """Run until score is updated by breaking a block"""
        for x, y, tile_id in iter_chunks(3, self.computer):
            if x == -1 and y == 0:
                self.score = tile_id
                break

            # Update frame buffer
            self.fb[(x, y)] = tile_id

            if tile_id == self.PADDLE:
                self.paddle = Coord(x, y)
            elif tile_id == self.BALL:
                prev_ball = self.ball
                self.ball = Coord(x, y)

                if self.ball_delta is None:
                    # We don't know the initial ball direction
                    self.ball_delta = Coord(0, 0)
                else:
                    self.ball_delta = self.ball - prev_ball
        else:
            # If we didn't break the computer was halted
            return False

        return True

    def run(self):
        """Run until halt and return final score"""
        while True:
            if not self.run_segment():
                return self.score


def solve(path):
    intcode = load_program_from_file(path)
    bot = Bot(intcode)
    return (find_num_blocks(intcode), bot.run())
