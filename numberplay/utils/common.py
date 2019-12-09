"""
Some common utils - these may be split into other modules when necessary.
"""
from typing import Any, Generator, Iterable, Sequence

def flatten(seq: Sequence[Iterable[Any]]) -> Generator[Any, None, None]:
    """
    Flatten a list by one level.

    flatten([[1, 4], [4]]) = [1, 4, 4]

    Parameters
    ----------
    seq : sequence(iterable(any))
        The list to flatten

    Returns
    -------
    generator(any, None, None)
        The flattened list.
    """
    return (item for subseq in seq for item in subseq)
