import math

from dataclasses import dataclass
from itertools import cycle, islice, takewhile

from .common import lines_from_file
from .plane import Coord, Vector


def vector_angle(vec):
    out = math.atan2(vec.dx, -vec.dy)
    if out < 0:
        return 2 * math.pi + out
    return out


class Map:
    def __init__(self, asteroids):
        self.asteroids = {Coord(x, y) for x, y in asteroids}
        self.width = max(x for x, _ in self.asteroids) + 1
        self.height = max(y for _, y in self.asteroids) + 1

    def __iter__(self):
        return iter(self.asteroids)

    def __str__(self):
        marker = {
            False: ".",
            True: "#",
        }
        return "\n".join(
            "".join(marker[Coord(x, y) in self.asteroids] for x in range(self.width))
            for y in range(self.height)
        )

    def in_bounds(self, coord):
        coord = Coord(*coord)
        return 0 <= coord.x < self.width and 0 <= coord.y < self.height

    @classmethod
    def from_lines(cls, m):
        return cls(
            Coord(x, y)
            for y, row in enumerate(m)
            for x, slot in enumerate(row)
            if slot == "#"
        )

    def get_rays(self, origin):
        """Return a set of unit vectors that can reach all asteroids.

        Incidentally the number of rays is the same as the number of visible
        asteroids.
        """
        origin = Coord(*origin)
        return {
            Vector.from_coords(origin, asteroid).normalize()
            for asteroid in self.asteroids
            if asteroid != origin
        }

    def iter_spinning_laser_targets(self, origin):
        origin = Coord(*origin)
        if origin not in self.asteroids:
            raise ValueError("Laser must be built on asteroid")

        # Copy since we are destructive
        asteroids = set(self.asteroids)
        asteroids.remove(origin)

        # Sort rays based on angle to ensure that we destroy them in order. We
        # sort this outside the loop since the rays never change
        rays = list(sorted(self.get_rays(origin), key=vector_angle))

        # Spin the laser of destruction forever (or until we break)
        for ray in cycle(rays):
            for target in takewhile(self.in_bounds, ray.iter_coords(origin)):
                if target not in asteroids:
                    continue

                asteroids.remove(target)
                yield target

                # If all asteroids are destroyed we can quit
                if not asteroids:
                    return
                break

    def detectable_asteroids(self, asteroid):
        """Number of asteroids that can be seen from this asteroid"""
        return len(self.get_rays(asteroid))


def solve(path):
    m = Map.from_lines(lines_from_file(path))

    (base_pos, base_score) = max(
        ((a, m.detectable_asteroids(a)) for a in m), key=lambda x: x[1],
    )
    destroyed_asteroids = m.iter_spinning_laser_targets(base_pos)

    asteroid_200 = next(islice(destroyed_asteroids, 199, 200))
    return (base_score, 100 * asteroid_200.x + asteroid_200.y)
