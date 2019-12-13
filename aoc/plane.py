import math
from dataclasses import dataclass, replace
from itertools import count


@dataclass(frozen=True)
class Coord:
    __slots__ = ("x", "y")

    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        if not isinstance(other, Coord):
            return NotImplemented
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Coord):
            return NotImplemented
        return Coord(self.x - other.x, self.y - other.y)

    def distance_from_origin(self):
        return abs(self.x) + abs(self.y)

    def up(self, steps=1):
        return replace(self, y=self.y - steps)

    def right(self, steps=1):
        return replace(self, x=self.x + steps)

    def down(self, steps=1):
        return replace(self, y=self.y + steps)

    def left(self, steps=1):
        return replace(self, x=self.x - steps)


@dataclass(init=False, frozen=True)
class Vector:
    __slots__ = ("dx", "dy")

    dx: int
    dy: int

    def __init__(self, dx: int, dy: int):
        if dx == 0 and dy == 0:
            raise ValueError(
                f"Tried to construct a vector with no direction ({dx}, {dy})"
            )
        object.__setattr__(self, "dx", dx)
        object.__setattr__(self, "dy", dy)

    @classmethod
    def from_coords(cls, origin: Coord, target):
        dx, dy = Coord(*target) - Coord(*origin)
        return cls(dx, dy)

    def normalize(self):
        # Find greatest common denominator to shorten the dx dy values to a unit
        # length. We use absolut value to ensure that all signs are preserved
        den = abs(math.gcd(self.dx, self.dy))
        return replace(self, dx=self.dx // den, dy=self.dy // den)

    def __iter__(self):
        yield self.dx
        yield self.dy

    def iter_coords(self, origin, include_origin=False):
        origin = Coord(*origin)
        if include_origin:
            yield origin
        for i in count(1):
            yield Coord(origin.x + i * self.dx, origin.y + i * self.dy)
