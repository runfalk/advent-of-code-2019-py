from .common import lines_from_file


def traverse_parents(orbits, planet):
    """Yields all ancestors to the given planet in ascending distance"""
    while planet in orbits:
        planet = orbits[planet]
        yield planet


def num_orbits(orbits):
    return sum(1 for c in orbits.keys() for _ in traverse_parents(orbits, c))


def num_transfers(orbits, a, b):
    # Build a lookup table for the transfer distance to each ancestor for A
    a_parents = {p: d for d, p in enumerate(traverse_parents(orbits, a))}

    # Find the closest common ancestor by iterating over B's ancestors
    for b_dist, b_parent in enumerate(traverse_parents(orbits, b)):
        if b_parent in a_parents:
            return a_parents[b_parent] + b_dist
    raise ValueError(f"No common ancestor between {a} and {b}")


def solve(path):
    orbit_pairs = (orbit.rstrip().split(")") for orbit in lines_from_file(path))
    orbits = {c: p for p, c in orbit_pairs}

    return (num_orbits(orbits), num_transfers(orbits, "YOU", "SAN"))
