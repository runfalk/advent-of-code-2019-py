from collections import deque, Counter, defaultdict
from itertools import combinations, count
from queue import PriorityQueue
from functools import lru_cache

from .common import lines_from_file
from .plane import Coord


def is_door(poi):
    return poi.isupper()


def find_paths(lines):
    # Used to give each robot a unique number
    player_counter = count()

    walls = set()
    pois = {}

    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            coord = Coord(x, y)
            if tile == "#":
                walls.add(coord)
            elif tile.isalpha():
                # Key or door
                pois[coord] = tile
            elif tile == "@":
                pois[coord] = str(next(player_counter))

    # Generate the shortest path from each point of interest to every other
    # point of interest but skip doors. We don't need doors since we just use
    # them to prevent us from taking a path until we have the correct key.
    # Robots (@) are considered as keys for this purpose
    paths = defaultdict(lambda: defaultdict(dict))
    for poi_coord, poi_name in pois.items():
        if is_door(poi_name):
            continue

        visited = set([poi_coord])
        to_explore = deque([[poi_coord]])
        while to_explore:
            path = to_explore.popleft()
            curr = path[-1]

            # If we have reach a point of interest we want to save it
            curr_name = pois.get(curr)
            if curr_name is not None:
                # We consider a key as required for this path if it passes
                # through a door belonging to a key, or the key itself
                required_keys = frozenset(
                    pois[c].lower()
                    for c in path
                    if c in pois and pois[c].isalpha() and pois[c] != curr_name
                )
                cost = len(path) - 1
                paths[poi_name][curr_name] = (cost, required_keys)

            for n in curr.iter_neighbors(walls | visited):
                visited.add(n)
                to_explore.append(path + [n])
    return paths


def tsp_solve(paths):
    @lru_cache(maxsize=10000)
    def min_cost(curr_pois, remaining):
        if not remaining:
            return 0

        # Go through every robot's current position and generate new possible
        # routes given that every one of them moves
        sub_costs = []
        for i, curr_poi in enumerate(curr_pois):
            for next_poi in paths[curr_poi]:
                # If the point of interest is already discovered we mustn't
                # check it again
                if next_poi not in remaining:
                    continue

                # If the path requires a key we still haven't aquired we can't
                # take that path
                cost, required_keys = paths[curr_poi][next_poi]
                if required_keys.intersection(remaining):
                    continue

                # Move this robot and recurse downwards
                next_pois = list(curr_pois)
                next_pois[i] = next_poi
                sub_cost = min_cost(tuple(next_pois), frozenset(remaining - {next_poi}))

                sub_costs.append(cost + sub_cost)

        return min(sub_costs)

    robots = frozenset(poi for poi in paths if poi.isdigit())
    return min_cost(tuple(robots), frozenset(paths) - robots)


def solve(path):
    maze_lines = [list(line) for line in lines_from_file(path)]
    graph_a = find_paths(maze_lines)

    # Update maze to change it into four separate mazes for part B
    at_pos = None
    for y in range(len(maze_lines)):
        if "@" in maze_lines[y]:
            at_pos = Coord(maze_lines[y].index("@"), y)
            break
    pattern_offset = at_pos - Coord(1, 1)
    pattern = [
        "@#@",
        "###",
        "@#@",
    ]
    for y in range(len(pattern)):
        for x in range(len(pattern[y])):
            maze_lines[pattern_offset.y + y][pattern_offset.x + x] = pattern[y][x]

    # Find graph for the part B maze
    graph_b = find_paths(maze_lines)

    return (tsp_solve(graph_a), tsp_solve(graph_b))
