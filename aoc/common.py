def iter_peek(it, include_last=False):
    it = iter(it)
    prev = next(it)

    for curr in it:
        yield (prev, curr)
        prev = curr

    if include_last:
        yield (prev, None)
