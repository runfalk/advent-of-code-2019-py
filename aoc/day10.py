import math
from math import atan2, gcd
from itertools import count


def count_iter(it):
    return sum(1 for _ in it)


def normalize_direction(dx, dy):
    den = gcd(dx, dy)
    dx //= abs(den)
    dy //= abs(den)
    return dx, dy


def ray_angle(ray):
    dx, dy = ray
    out = math.atan2(dx, -dy)
    if out < 0:
        return 2 * math.pi + out
    return out


class Map:
    def __init__(self, asteroids):
        asteroids = list(asteroids)
        self.width = max(x for x, _ in asteroids) + 1
        self.height = max(y for _, y in asteroids) + 1
        self.asteroids = set(asteroids)

    def __iter__(self):
        return iter(self.asteroids)

    def __contains__(self, other):
        return other in self.asteroids

    def __len__(self):
        return len(self.asteroids)

    def __str__(self):
        marker = {
            False: ".",
            True: "#",
        }
        return "\n".join(
            "".join(marker[(x, y) in self.asteroids] for x in range(self.width))
            for y in range(self.height)
        )

    def is_oob(self, asteroid):
        x, y = asteroid
        in_bounds = 0 <= x < self.width and 0 <= y < self.height
        return not in_bounds

    @classmethod
    def from_str_map(cls, m):
        return cls(
            (x, y)
            for y, row in enumerate(m)
            for x, slot in enumerate(row)
            if slot == "#"
        )

    def get_rays(self, origin):
        deltas = {
            normalize_direction(x - origin[0], y - origin[1])
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) != origin
        }
        ordered_deltas = list(sorted(deltas, key=ray_angle))
        return ordered_deltas

    def iter_spinning_laser_targets(self, origin):
        if origin not in self.asteroids:
            raise ValueError("Laser must be built on asteroid")

        # Copy since we are destructive
        asteroids = set(self.asteroids)
        asteroids.remove(origin)

        rays = self.get_rays(origin)
        while asteroids:
            for dx, dy in rays:
                for i in count(1):
                    target = (
                        i * dx + origin[0],
                        i * dy + origin[1],
                    )
                    if target in asteroids:
                        asteroids.remove(target)
                        yield target
                        break
                    elif self.is_oob(target):
                        break

    def iter_blocked_coords(self, asteroid):
        if asteroid not in self.asteroids:
            raise KeyError("No such asteroid")

        # We can't see ourselves
        yield asteroid

        for other in self.asteroids:
            if other == asteroid:
                continue

            dx, dy = normalize_direction(other[0] - asteroid[0], other[1] - asteroid[1])

            for i in count(1):
                blocked_pos = (
                    i * dx + other[0],
                    i * dy + other[1],
                )
                if self.is_oob(blocked_pos):
                    break
                yield blocked_pos

    def detectable_asteroids(self, asteroid):
        blocked = set(self.iter_blocked_coords(asteroid))
        return len(self.asteroids - blocked)


def solve(path):
    with open(path) as f:
        m = Map.from_str_map(f)

    (base_pos, base_score) = max(
        ((a, m.detectable_asteroids(a)) for a in m), key=lambda x: x[1],
    )
    order = list(m.iter_spinning_laser_targets(base_pos))

    return (base_score, 100 * order[199][0] + order[199][1])
