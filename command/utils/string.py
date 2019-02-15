from itertools import chain


def multifind(s: str, items: set, start=0):
    """Finds the first occurance of an item in `items` in `s`, and return the start and end indices."""
    items_lengths = set(len(i) for i in items)
    slices = ((slice(b, b+e) for e in items_lengths) for b in range(start, len(s)))  # O(len(items) * len(s))

    for sl in chain.from_iterable(slices):
        if s[sl] in items:
            return (sl.start, sl.stop)

    return (len(s), len(s))


def multisplit(s: str, delims: set, max_split=-1, filter_empty=True):
    rv = []

    last_end = 0
    while max_split != 0:
        b, e = multifind(s, delims, last_end)

        if not filter_empty or last_end != b:
            rv.append(s[last_end:b])
            max_split -= 1

        if b == len(s) and e == len(s):
            break

        last_end = e

    return rv
