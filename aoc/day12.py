import re
import math

from itertools import combinations, islice
from dataclasses import dataclass, replace

from .common import lines_from_file


def lcm(a, b):
    """Return lowest common multiple.

    This means the smallest possible number that is evenly divisible by both A
    and B. It is very useful when determining cycle lengths for combinations of
    sequences of different cycle lengths.

    Imagine two sequences of different lengths:

        from itertools import cycle
        a = range(2)
        b = range(3)
        len_cycle = sum(1 for _ in a for _ in b)  # 2 * 3 = 6
        assert lcm(len(a), len(b)) == len_cycle

    """
    return a * b // math.gcd(a, b)


def cmp(a, b):
    """Reimplementation of Python 2's C style cmp function"""
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


@dataclass(frozen=True)
class Coord:
    __slots__ = ("x", "y", "z")

    x: int
    y: int
    z: int

    @classmethod
    def origin(cls):
        return cls(0, 0, 0)

    @classmethod
    def from_str(cls, s):
        m = re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", s)
        if m is None:
            raise ValueError("This is no moon")
        return cls(int(m.group(1)), int(m.group(2)), int(m.group(3)),)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other):
        if not isinstance(other, Coord):
            return NotImplemented
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if not isinstance(other, Coord):
            return NotImplemented
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance_to(self, other):
        return sum(map(abs, self - other))


@dataclass(frozen=True)
class Moon:
    __slots__ = ("pos", "vel")

    pos: Coord
    vel: Coord

    def __init__(self, pos, vel=None):
        object.__setattr__(self, "pos", pos)
        if vel is None:
            vel = Coord.origin()
        object.__setattr__(self, "vel", vel)

    @property
    def potential_energy(self):
        return self.pos.distance_to(Coord.origin())

    @property
    def kinetic_energy(self):
        return self.vel.distance_to(Coord.origin())

    @property
    def energy(self):
        return self.potential_energy * self.kinetic_energy

    def step(self):
        return replace(self, pos=self.pos + self.vel)

    @classmethod
    def apply_gravity(cls, a, b):
        a_delta_vel = Coord(*(-cmp(apos, bpos) for apos, bpos in zip(a.pos, b.pos)))

        return (
            replace(a, vel=a.vel + a_delta_vel),
            replace(b, vel=b.vel - a_delta_vel),
        )


def iter_system(system):
    system = list(system)
    while True:
        for ia, ib in combinations(range(len(system)), r=2):
            system[ia], system[ib] = Moon.apply_gravity(system[ia], system[ib])

        for i in range(len(system)):
            system[i] = system[i].step()

        yield tuple(system)


def run_until_repetition(system):
    # Track repetitions in each dimensions, since they are completely
    # independent
    prev_x = set()
    prev_y = set()
    prev_z = set()

    for new_system in iter_system(system):
        x_system = tuple((m.pos.x, m.vel.x) for m in new_system)
        y_system = tuple((m.pos.y, m.vel.y) for m in new_system)
        z_system = tuple((m.pos.z, m.vel.z) for m in new_system)

        # Once we have detected repetions for each dimension we use LCM to
        # determine the full cycle length
        if x_system in prev_x and y_system in prev_y and z_system in prev_z:
            return lcm(lcm(len(prev_x), len(prev_y)), len(prev_z))

        prev_x.add(x_system)
        prev_y.add(y_system)
        prev_z.add(z_system)


def solve(path):
    system = [Moon(Coord.from_str(line)) for line in lines_from_file(path)]

    a = sum(moon.energy for moon in next(islice(iter_system(system), 999, 1000)))
    b = run_until_repetition(system)

    return (a, b)
