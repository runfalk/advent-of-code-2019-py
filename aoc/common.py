from itertools import count


def lines_from_file(path):
    with open(path) as f:
        for line in f:
            # Remove trailing whitespace
            yield line.rstrip("\r\n")


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
