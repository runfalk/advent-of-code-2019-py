from .common import lines_from_file


def get_fuel_req(mass):
    out = mass // 3 - 2
    if out < 0:
        out = 0
    return out


def get_fuel_load_req(mass):
    total = 0
    while mass > 0:
        mass = get_fuel_req(mass)
        total += mass
    return total


def solve(path):
    modules_masses = list(map(int, lines_from_file(path)))
    return (
        sum(get_fuel_req(m) for m in modules_masses),
        sum(get_fuel_load_req(m) for m in modules_masses),
    )
