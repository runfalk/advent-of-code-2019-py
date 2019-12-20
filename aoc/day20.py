from collections import deque, defaultdict
from dataclasses import dataclass, field
from operator import attrgetter

from .common import lines_from_file, PriorityQueue
from .plane import Coord


def find_label(tiles, coord):
    # Only paths can have labels
    if tiles[coord] != ".":
        return None

    for n in coord.iter_neighbors():
        n_tile = tiles.get(n)
        if n_tile is None or not n_tile.isalpha():
            continue
        label_coords = [tuple(n), tuple(n - coord + n)]
        return "".join(tiles[Coord(x, y)] for x, y in sorted(label_coords))


def find_coord_min_max(it):
    it = iter(it)
    min_x, min_y = next(it)
    max_x = min_x
    max_y = min_y

    for x, y in it:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
    return Coord(min_x, min_y), Coord(max_x, max_y)


def find_portals(lines):
    # Extract all non-whitespace tiles into a dict from coordinates to chars
    tiles = {
        Coord(x, y): tile
        for y, line in enumerate(lines)
        for x, tile in enumerate(line)
        if tile != " "
    }

    # Find walls and labels for portals
    walls = set()
    portal_labels = {}
    for coord, tile in tiles.items():
        # Wall or label
        if tile != ".":
            walls.add(coord)

        label = find_label(tiles, coord)
        if label is not None:
            portal_labels[coord] = label

    # Helper function to check if a portal is on the outer or inner edge
    path_min, path_max = find_coord_min_max(portal_labels)

    def is_inner(coord):
        return path_min.x < coord.x < path_max.x and path_min.y < coord.y < path_max.y

    # Calculate the cost from every portal to every other portal it can reach
    portals = {}
    for start, source_label in portal_labels.items():
        to_portals = {}
        visited = set([start])
        to_explore = deque([(0, start)])
        while to_explore:
            cost, curr = to_explore.popleft()
            if curr in portal_labels and cost:
                to_portals[(portal_labels[curr], is_inner(curr))] = cost
            for n in curr.iter_neighbors(blacklist=visited | walls):
                visited.add(n)
                to_explore.append((cost + 1, n))
        portals[(source_label, is_inner(start))] = to_portals
    return portals


@dataclass
class Portal:
    name: str
    cost: int = field(default=0)
    is_inner: bool = field(default=False)
    layer: int = field(default=0)

    def key(self, invert=False):
        return (self.name, self.is_inner != invert)

    def next(self, name, cost, is_inner):
        return Portal(
            name,
            self.cost + cost + 1,
            not is_inner,
            self.layer + (1 if is_inner else -1),
        )


def shortest_path(portals, *, recursive=False):
    start_portal = Portal("AA")
    end_portal = Portal("ZZ")

    # We use a separate visited set per layer
    used_portals = defaultdict(set)
    if recursive:
        used_portals = defaultdict(lambda: set([start_portal.key(), end_portal.key()]))
        for name, is_inner in portals:
            if not is_inner:
                used_portals[0].add((name, is_inner))
        used_portals[0].discard(end_portal.key())

    to_explore = PriorityQueue(cost_func=attrgetter("cost"))
    to_explore.put(start_portal)

    while to_explore:
        curr_portal = to_explore.get()
        if curr_portal.name == "ZZ":
            # We remove one since we never entered the portal
            return curr_portal.cost - 1

        next_portals = portals.get((curr_portal.name, curr_portal.is_inner), {})
        for (name, is_inner), cost in next_portals.items():
            next_portal = curr_portal.next(name, cost, is_inner)

            next_portal_key = next_portal.key(invert=True)
            if next_portal_key in used_portals[curr_portal.layer]:
                continue

            used_portals[curr_portal.layer].add(next_portal_key)
            to_explore.put(next_portal)


def solve(path):
    portals = find_portals(lines_from_file(path))
    return (shortest_path(portals), shortest_path(portals, recursive=True))
