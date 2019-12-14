import bisect

from collections import defaultdict
from fractions import Fraction

# Number of available ores for part B
ORE_LIMIT = 1_000_000_000_000


class Reaction:
    def __init__(self, min_quantity, components):
        self.min_quantity = min_quantity
        if isinstance(components, dict):
            components = components.items()
        self.components = {name: quantity for name, quantity in components}
        self.norm_components = {
            name: Fraction(quantity, min_quantity)
            for name, quantity in self.components.items()
        }

    @classmethod
    def pair_from_str(cls, s):
        def parse_pair(s):
            x, y = s.split(" ")
            return int(x), y

        sources_str, result_str = s.split(" => ")
        result_quantity, result_name = parse_pair(result_str)
        return (
            result_name,
            cls(
                result_quantity,
                [
                    tuple(reversed(parse_pair(source)))
                    for source in sources_str.split(", ")
                ],
            ),
        )

    def __repr__(self):
        return f"Reaction(min_quantity={self.min_quantity}, components={self.components!r})"


# Hack to implement binary search of ore requirements
class FuelFinder:
    def __init__(self, reactions, num_ores):
        self.reactions = reactions
        self.norm_order = list(find_normalization_order(reactions))
        self.num_ores = num_ores
        self._len = 2 * self.num_ores // find_required_ores(self.reactions)

    def __getitem__(self, fuel_quantity):
        return find_required_ores(self.reactions, fuel_quantity, self.norm_order)

    def __len__(self):
        return self._len

    def find(self):
        i = bisect.bisect_left(self, self.num_ores, lo=1)
        return i - 1


def find_min_requirements(reactions, name, quantity):
    reaction = reactions.get(name)
    if reaction is None:
        # This happens when name is ORE
        return

    for cname, cquantity in reaction.norm_components.items():
        yield (cname, quantity * cquantity)
        yield from find_min_requirements(reactions, cname, quantity * cquantity)


def find_normalization_order(reactions):
    component_to_reactions = defaultdict(set)
    for name, reaction in reactions.items():
        for cname in reaction.components:
            component_to_reactions[cname].add(name)

    remaining_components = set(reactions.keys())
    while remaining_components:
        for cname in list(remaining_components):
            # Check if component is still in use
            if component_to_reactions[cname]:
                continue

            for reactions in component_to_reactions.values():
                reactions.discard(cname)
            remaining_components.discard(cname)
            yield cname


def find_required_ores(reactions, fuel_quantity=1, norm_order=None):
    if norm_order is None:
        norm_order = list(find_normalization_order(reactions))

    # Find number of resources required using normalized recipes. A normalized
    # recipe is a recipe where the result is one unit
    min_reqs = defaultdict(int)
    for name, quantity in find_min_requirements(reactions, "FUEL", fuel_quantity):
        min_reqs[name] += quantity

    # Since we can't use normalized recipes for the result we must add resource
    # requirements until all resources reach a multiple of their minimum
    # quantity. If we consider recipes as a tree structure with FUEL at the root
    # and ORE as the leaves we must do this in an order such that a node must
    # never be updated by an ancestor after it's been processed
    for name in norm_order:
        quantity = min_reqs[name]
        min_quantity = reactions[name].min_quantity
        rem = quantity % min_quantity
        if rem == 0:
            continue

        for n, q in find_min_requirements(reactions, name, min_quantity - rem):
            min_reqs[n] += q
        min_reqs[name] += rem

    return int(min_reqs["ORE"])


def solve(path):
    with open(path) as f:
        lines = (line.rstrip() for line in f)
        reactions = dict(map(Reaction.pair_from_str, lines))

    return (
        find_required_ores(reactions),
        FuelFinder(reactions, 1_000_000_000_000).find(),
    )
