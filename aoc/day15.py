import asyncio

from collections import deque
from itertools import count

from .common import dict_coords_as_str
from .day9 import Interpreter
from .intcode import load_program_from_file
from .plane import Coord


def debug_render(explored, droid):
    pixels = dict(explored.items())
    pixels[droid] = 3
    return dict_coords_as_str(pixels, {None: " ", 0: "#", 1: ".", 2: "X", 3: "o"})


class Maze:
    def __init__(self, walls):
        self.walls = set(walls)

    def __eq__(self, other):
        if isinstance(other, Maze):
            return self.walls == other.walls
        return NotImplemented

    def find_neighbors(self, pos, *, blacklist=None):
        if blacklist is None:
            blacklist = set()
        yield from pos.iter_neighbors(blacklist=self.walls | set(blacklist))

    def shortest_path(self, start, end):
        """Return the shortest path between start and end (start excluded)"""
        explored = set([start])
        unexplored = deque([[start]])
        while unexplored:
            path = unexplored.popleft()

            curr = path[-1]
            if curr == end:
                # Skip starting element
                return path[1:]

            for n in self.find_neighbors(curr, blacklist=explored):
                explored.add(n)
                unexplored.append(path + [n])

    def longest_shortest_path(self, start):
        """
        Explore the shortest path to every point in the maze from the given
        start and return path to the furthest away point. If multiple points
        have the same distance any of them may be returned.
        """
        # Iterate breadth first to ensure that we always find the shortest path
        # to every point
        longest_path = []
        explored = set([start])
        unexplored = deque([[start]])
        while unexplored:
            path = unexplored.popleft()
            curr = path[-1]

            if len(longest_path) < len(path):
                longest_path = path

            for n in self.find_neighbors(curr, blacklist=explored):
                explored.add(n)
                unexplored.append(path + [n])

        # Skip starting element
        return longest_path[1:]


class Droid:
    """
    Control interface for the repair droid. The given queues must be connected
    to an intcode interpreter
    """

    reverse_cmds = {
        1: 2,
        2: 1,
        3: 4,
        4: 3,
    }

    def __init__(self, cmd_queue, status_queue, start=None):
        if start is None:
            start = Coord(0, 0)
        self.pos = start
        self.cmds = cmd_queue
        self.status = status_queue

    def peek_move(self, cmd):
        if cmd == 1:
            return self.pos.up()
        elif cmd == 2:
            return self.pos.down()
        elif cmd == 3:
            return self.pos.left()
        elif cmd == 4:
            return self.pos.right()
        raise ValueError(f"Unknown droid command {cmd!r}")

    def iter_moves(self, blacklist=None):
        if blacklist is None:
            blacklist = set()

        for cmd in range(1, 5):
            pos = self.peek_move(cmd)
            if pos not in blacklist:
                yield (cmd, pos)

    async def move(self, cmd):
        await self.cmds.put(cmd)
        status = await self.status.get()
        if status != 0:
            self.pos = self.peek_move(cmd)
        return status

    async def reverse_move(self, cmd):
        return await self.move(self.reverse_cmds[cmd])


async def explore_maze(intcode, debug=False):
    cmds = asyncio.Queue()
    status = asyncio.Queue()
    droid = Droid(cmds, status)
    computer_task = asyncio.create_task(
        Interpreter.async_run_program(intcode, cmds, status)
    )

    goal = None
    tiles = {}
    steps = []

    for i in count(1):
        if debug:
            print(debug_render(tiles, droid.pos))
            print("Iteration:", i)

        # Find next move or None if we are in a dead end. Any valid move will do
        cmd, next_pos = next(droid.iter_moves(blacklist=tiles), (None, None))

        # Check if we're out of movement options for this tile
        if cmd is None:
            # If we can't backtrack that means we have explored everything
            if not steps:
                break

            # We backtrack one step
            status = await droid.reverse_move(steps.pop())
            continue

        status = await droid.move(cmd)
        tiles[next_pos] = status
        if status != 0:
            # Only modify the steps for backtracking if we actually moved
            steps.append(cmd)

        if status == 2:
            goal = droid.pos

    await Interpreter.shutdown_async_program(computer_task)
    return Maze(coord for coord, tile in tiles.items() if tile == 0), goal


def solve(path):
    intcode = load_program_from_file(path)
    start = Coord(0, 0)
    maze, oxygen_system = asyncio.run(explore_maze(intcode))
    return (
        len(maze.shortest_path(start, oxygen_system)),
        len(maze.longest_shortest_path(oxygen_system)),
    )
