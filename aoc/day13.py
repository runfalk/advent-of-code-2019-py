from collections import Counter
from itertools import count

from .common import dict_coords_as_str
from .day12 import cmp
from .day8 import iter_chunks
from .day9 import Interpreter
from .intcode import load_program_from_file
from .plane import Coord


EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

debug_colors = {
    EMPTY: " ",
    WALL: "#",
    BLOCK: "X",
    PADDLE: "_",
    BALL: "o",
}


def find_num_blocks(intcode):
    computer = Interpreter.run_program(intcode)
    tiles = Counter(tile_id for _, _, tile_id in iter_chunks(3, computer))
    return tiles[BLOCK]


def play_game(intcode, debug=False):
    framebuffer = {}
    score = 0
    ball = Coord(0, 0)
    paddle = Coord(0, 0)

    def joystick():
        for i in count():
            move = cmp(0, paddle.x - ball.x)
            if debug:
                print(dict_coords_as_str(framebuffer, debug_colors))
                print("Iteration:", i)
                print("Paddle:", paddle)
                print("Ball:", ball)
                print("Move:", move)
                print("Score:", score)
            yield move

    # Put the game in free to play mode
    intcode = list(intcode)
    intcode[0] = 2

    computer = Interpreter.run_program(intcode, joystick())
    for x, y, tile_id in iter_chunks(3, computer):
        if x == -1 and y == 0:
            score = tile_id
            continue

        framebuffer[(x, y)] = tile_id
        if tile_id == PADDLE:
            paddle = Coord(x, y)
        elif tile_id == BALL:
            ball = Coord(x, y)

    return score


def solve(path):
    intcode = load_program_from_file(path)
    return (find_num_blocks(intcode), play_game(intcode))
