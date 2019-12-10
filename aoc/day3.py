from .plane import Coord


def follow(path):
    curr = Coord(0, 0)
    for move in path:
        steps = int(move[1:])
        action = {"U": curr.up, "R": curr.right, "D": curr.down, "L": curr.left,}[
            move[0]
        ]

        for i in range(steps):
            yield action(i + 1)
        curr = action(steps)


def solve(path):
    with open(path) as f:
        wire_a = next(f).rstrip().split(",")
        wire_b = next(f).rstrip().split(",")

    wire_a_steps = {
        coord: num_steps for num_steps, coord in enumerate(follow(wire_a), 1)
    }

    intersect_coords = []
    intersect_steps = []
    for num_steps, coord in enumerate(follow(wire_b), 1):
        if coord in wire_a_steps:
            intersect_coords.append(coord)
            intersect_steps.append(wire_a_steps[coord] + num_steps)

    return (
        min(c.distance_from_origin() for c in intersect_coords),
        min(intersect_steps),
    )
