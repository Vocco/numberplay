"""
TODO: Add docstring.
"""
import functools as ft
import math
import multiprocessing as mp
from typing import Generator, Iterable, List, Set

from numberplay.utils import parallel as p


def find_proper_divisors(number: int) -> Generator[int, None, None]:
    """
    TODO: Add docstring.

    FIXME: Returns 1 2 3 3 2 for 6
    """
    return __get_divisors_from_chunk(range(2, math.ceil(math.sqrt(number)) + 1), number)


def find_proper_divisors_parallel(number: int, processes=1) -> List[int]:
    """
    TODO: Add docstring.
    """
    pool = mp.Pool(processes)
    found: List[int] = []

    for chunk_start, chunk_end in p.get_chunk_indices(2, math.ceil(math.sqrt(number)), processes):
        pool.apply_async(
            __find_proper_divisors_in_chunk,
            args=(range(chunk_start, chunk_end), number),
            callback=p.collect_result(found))

    pool.close()
    pool.join()

    return sorted(ft.reduce(lambda all_found, new_found: all_found.union(new_found), found, set()))




def __get_divisors_from_chunk(chunk, number):
    """
    TODO: Add docstring.
    """
    yield 1
    for divisor_candidate in chunk:

        if not number % divisor_candidate:
            yield divisor_candidate

            division_counterpart = number // divisor_candidate
            if division_counterpart != divisor_candidate:
                yield division_counterpart



def __find_proper_divisors_in_chunk(chunk: Iterable[int], number: int) -> Set[int]:
    """
    TODO: Add docstring.
    """
    return set(__get_divisors_from_chunk(chunk, number))
