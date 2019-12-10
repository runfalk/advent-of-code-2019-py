import math

from itertools import count, cycle, islice

from .common import Coord


class Ray:
    __slots__ = ("dx", "dy")

    def __init__(self, dx, dy):
        # Find greatest common denominator to shorten the dx dy values to a unit
        # length. We use absolut value to ensure that all signs are preserved
        den = abs(math.gcd(dx, dy))

        if not den:
            raise ValueError(f"Tried to construct a ray with no direction ({dx}, {dy})")

        # Shorten the input ray to the unit length
        self.dx = dx // den
        self.dy = dy // den

    @classmethod
    def from_coords(cls, origin, target):
        dx, dy = Coord(*target) - Coord(*origin)
        return cls(dx, dy)

    @property
    def angle(self):
        """Angle in radians clockwise based on the up direction.

        This assumes a coordinate system where up is negative Y and right is
        positive X.
        """
        out = math.atan2(self.dx, -self.dy)
        if out < 0:
            return 2 * math.pi + out
        return out

    def __iter__(self):
        yield self.dx
        yield self.dy

    def __repr__(self):
        return "Ray(dx={}, dy={})".format(self.dx, self.dy)

    def __hash__(self):
        return hash((self.dx, self.dy))

    def __eq__(self, other):
        if not isinstance(other, Ray):
            return NotImplemented
        return self.dx == other.dx and self.dy == other.dy

    def __ne__(self, other):
        if not isinstance(other, Coord):
            return NotImplemented
        return not (self == other)

    def iter_coords(self, origin, include_origin=False):
        origin = Coord(*origin)
        for i in count(0 if include_origin else 1):
            yield Coord(origin.x + i * self.dx, origin.y + i * self.dy)


class Map:
    def __init__(self, asteroids):
        self.asteroids = {Coord(*a) for a in asteroids}
        self.width = max(x for x, _ in self.asteroids) + 1
        self.height = max(y for _, y in self.asteroids) + 1

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
            "".join(marker[Coord(x, y) in self.asteroids] for x in range(self.width))
            for y in range(self.height)
        )

    def is_oob(self, asteroid):
        asteroid = Coord(*asteroid)
        in_bounds = 0 <= asteroid.x < self.width and 0 <= asteroid.y < self.height
        return not in_bounds

    @classmethod
    def from_str_map(cls, m):
        return cls(
            Coord(x, y)
            for y, row in enumerate(m)
            for x, slot in enumerate(row)
            if slot == "#"
        )

    def get_rays(self, origin):
        """Return a set of rays that can reach all asteroids in this map"""
        return {
            Ray.from_coords(origin, (x, y))
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) != tuple(origin)
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
        rays = list(sorted(self.get_rays(origin), key=lambda ray: ray.angle))

        # Spin the laser of destruction forever (or until we break)
        for ray in cycle(rays):
            for target in ray.iter_coords(origin):
                if self.is_oob(target):
                    break
                elif target in asteroids:
                    asteroids.remove(target)
                    yield target

                    # If all asteroids are destroyed we can quit
                    if not asteroids:
                        return
                    break

    def iter_blocked_coords(self, origin):
        """Iterate all coordinates that are blocked from this coordinate.

        Note that the asteroids we have a direct line of sight to are not
        included.
        """
        if origin not in self.asteroids:
            raise KeyError(f"No such asteroid {origin!r}")

        for other in self.asteroids:
            if other == origin:
                continue

            ray = Ray.from_coords(origin, target=other)
            for blocked_pos in ray.iter_coords(origin=other):
                if self.is_oob(blocked_pos):
                    break
                yield blocked_pos

    def detectable_asteroids(self, asteroid):
        blocked = set(self.iter_blocked_coords(asteroid))
        return len(self.asteroids - blocked - {asteroid})


def solve(path):
    with open(path) as f:
        m = Map.from_str_map(f)

    (base_pos, base_score) = max(
        ((a, m.detectable_asteroids(a)) for a in m), key=lambda x: x[1],
    )
    destroyed_asteroids = m.iter_spinning_laser_targets(base_pos)

    asteroid_200 = next(islice(destroyed_asteroids, 199, 200))
    return (base_score, 100 * asteroid_200.x + asteroid_200.y)
