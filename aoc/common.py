from itertools import count


class Coord:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self):
        return "Coord(x={}, y={})".format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, Coord):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        if not isinstance(other, Coord):
            return NotImplemented
        return self.x != other.x or self.y != other.y

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

    def up(self, steps):
        return Coord(self.x, self.y + steps)

    def right(self, steps):
        return Coord(self.x + steps, self.y)

    def down(self, steps):
        return Coord(self.x, self.y - steps)

    def left(self, steps):
        return Coord(self.x - steps, self.y)


class Digits:
    __slots__ = ("value", "base")

    def __init__(self, value, base=10):
        self.value = value
        self.base = base

    def __len__(self):
        """Return the number of digits in this number"""
        v = self.value
        for i in count():
            if v == 0:
                return i
            v //= self.base

    def __getitem__(self, i):
        if i < 0:
            i = len(self) + i
        return (self.value // self.base ** i) % self.base

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]


def last(it):
    """Return the last value of the given iterator"""
    output = None
    for item in it:
        output = item
    return output


def iter_peek(it, include_last=False):
    it = iter(it)
    prev = next(it)

    for curr in it:
        yield (prev, curr)
        prev = curr

    if include_last:
        yield (prev, None)
