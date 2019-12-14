from .common import lines_from_file


def traverse_parents(orbits, planet):
    while planet in orbits:
        planet = orbits[planet]
        yield planet


def num_orbits(orbits):
    return sum(1 for c in orbits.keys() for _ in traverse_parents(orbits, c))


def num_transfers(orbits, a, b):
    # Build lookup tables for the transfer distance to each ancestor
    a_parents = {p: d for d, p in enumerate(traverse_parents(orbits, a))}
    b_parents = {p: d for d, p in enumerate(traverse_parents(orbits, b))}

    # Find the closest common ancestor
    common_ancestors = set(a_parents).intersection(set(b_parents))
    common_ancestor = min(common_ancestors, key=lambda x: a_parents[x] + b_parents[x])

    # Return the number of transfers between A and B
    return a_parents[common_ancestor] + b_parents[common_ancestor]


def solve(path):
    orbit_pairs = (orbit.rstrip().split(")") for orbit in lines_from_file(path))
    orbits = {c: p for p, c in orbit_pairs}

    return (num_orbits(orbits), num_transfers(orbits, "YOU", "SAN"))
