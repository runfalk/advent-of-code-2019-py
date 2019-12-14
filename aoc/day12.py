import math
import re

from dataclasses import dataclass
from functools import reduce
from itertools import combinations, count

from .common import lines_from_file


def cycle_len(*cycle_lens):
    """Calculate combined cycle length using lowest common multiple"""
    return reduce(lambda a, b: a * b // math.gcd(a, b), cycle_lens)


def cmp(a, b):
    """Reimplementation of Python 2's C style cmp function"""
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


def parse_coord(s):
    m = re.match(r"<x=\s*(-?\d+), y=\s*(-?\d+), z=\s*(-?\d+)>", s)
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


@dataclass(frozen=True)
class Moon:
    x: int
    y: int
    z: int
    dx: int = 0
    dy: int = 0
    dz: int = 0

    @classmethod
    def from_str(cls, s):
        return cls(*parse_coord(s))

    @property
    def energy(self):
        potential_energy = abs(self.x) + abs(self.y) + abs(self.z)
        kinetic_energy = abs(self.dx) + abs(self.dy) + abs(self.dz)
        return potential_energy * kinetic_energy


class AxisTimeline:
    """Simulates moons along a single axis"""

    def __init__(self, moons):
        self._moons = list(moons)
        self._cycle_detected = False
        self._iterations = [tuple(self._moons)]

    def _simulate(self, max_iteration=None):
        for i in count(len(self._iterations)):
            if max_iteration is not None and i > max_iteration:
                break

            # Apply gravity to change moon state
            for ia, ib in combinations(range(len(self._moons)), r=2):
                pa, va = self._moons[ia]
                pb, vb = self._moons[ib]
                self._moons[ia] = (pa, va + cmp(pb, pa))
                self._moons[ib] = (pb, vb - cmp(pb, pa))

            # Update moon positions
            for i, (p, v) in enumerate(self._moons):
                self._moons[i] = (p + v, v)

            moons = tuple(self._moons)
            if moons == self._iterations[0]:
                self._cycle_detected = True
                break

            self._iterations.append(moons)

    def __getitem__(self, iteration):
        if self._cycle_detected:
            iteration = iteration % len(self._iterations)

        if iteration < len(self._iterations):
            return self._iterations[iteration]

        self._simulate(max_iteration=iteration)
        return self._iterations[iteration]

    def cycle_len(self):
        if not self._cycle_detected:
            self._simulate()
        return len(self._iterations)


class SpaceTimeline:
    """Provides access to 3D state for any given time using AxisTimelines"""

    def __init__(self, moons):
        moons = list(moons)
        self.x_axis = AxisTimeline((moon.x, moon.dx) for moon in moons)
        self.y_axis = AxisTimeline((moon.y, moon.dy) for moon in moons)
        self.z_axis = AxisTimeline((moon.z, moon.dz) for moon in moons)

    def __getitem__(self, i):
        tuple_moons = list(zip(self.x_axis[i], self.y_axis[i], self.z_axis[i]))
        return tuple(
            Moon(
                *(tm[axis][value_type] for value_type in range(2) for axis in range(3))
            )
            for tm in tuple_moons
        )

    def cycle_len(self):
        return cycle_len(
            self.x_axis.cycle_len(), self.y_axis.cycle_len(), self.z_axis.cycle_len(),
        )


def solve(path):
    timeline = SpaceTimeline(Moon.from_str(line) for line in lines_from_file(path))
    return (sum(m.energy for m in timeline[1000]), timeline.cycle_len())
