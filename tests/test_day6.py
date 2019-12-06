from aoc.day6 import num_orbits, num_transfers, solve


orbit_pairs = [
    "COM)B",
    "B)C",
    "C)D",
    "D)E",
    "E)F",
    "B)G",
    "G)H",
    "D)I",
    "E)J",
    "J)K",
    "K)L",
]


def get_orbits(orbit_pairs):
    return dict(tuple(reversed(pair.split(")"))) for pair in orbit_pairs)


def test_num_orbits():
    orbits = get_orbits(orbit_pairs)
    assert num_orbits(orbits) == 42


def test_num_transfers():
    orbits = get_orbits(orbit_pairs + ["K)YOU", "I)SAN"])
    assert num_transfers(orbits, "YOU", "SAN") == 4


def test_solve():
    assert solve("data/day6.txt") == (171213, 292)
