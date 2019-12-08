"""
Functions to find narcissistic numbers.
"""
import functools as ft
import multiprocessing as mp
from typing import Callable, Iterable, List

from numberplay.utils import digits as d
from numberplay.utils import parallel as p


def __get_narcissistic_filter(num_digits: int) -> Callable[[int], bool]:
    """
    Initialize a function which determines whether a number is narcissistic.

    Parameters
    ----------
    num_digits : integer
        The number of digits of the numbers which will be input to the resulting function.

    Returns
    -------
    integer -> boolean
        A function which determines if an input number is narcissistic. Guaranteed to work properly
        only on nonnegative inputs with `num_digits` digits.
    """
    def narcissistic_filter(number: int) -> bool:
        return number == ft.reduce(
            lambda current_sum, digit: current_sum + digit ** num_digits, d.digit_split(number), 0)

    return narcissistic_filter


def __get_narcissistic_for_chunk(chunk: Iterable[int], num_digits: int) -> List[int]:
    """
    Return a list of narcissistic numbers from a chunk of numbers.

    Parameters
    ----------
    chunk : iterable(integer)
        An iterable of nonnegative integers with `num_digits` digits.
    num_digits : integer
        The number of digits of the numbers in `chunk`.

    Returns
    -------
    list(integer)
        A list of all narcissistic integers in `chunk`.
    """
    return list(filter(__get_narcissistic_filter(num_digits), chunk))


def is_narcissistic(number: int) -> bool:
    """
    Determine whether a number is narcissistic.

    Parameters
    ----------
    number : integer
        A positive integer.

    Returns
    -------
    boolean
        True when `number` is narcissistic, False otherwise.
    """
    num_digits = len(list(d.digit_split(number)))
    return __get_narcissistic_filter(num_digits)(number)


def find_narcissistic_numbers(num_digits: int) -> List[int]:
    """
    Find all narcissistic numbers with `num_digits` digits.

    It is highly recommended to use `find_narcissistic_numbers_parallel` to search for narcissistic
    numbers of more than 5 digits, as the space to search is grows exponentially with respect to
    the parameter.

    Parameters
    ----------
    num_digits : integer
        The number of digits of the narcissistic numbers to find.

    Returns
    -------
    list(integer)
        An list over all the narcissistic numbers with `num_digits` digits in increasing order.
    """
    return list(
        filter(
            __get_narcissistic_filter(num_digits),
            range(d.lowest_n_digit_number(num_digits), d.highest_n_digit_number(num_digits) + 1)))


def find_narcissistic_numbers_parallel(num_digits: int, processes=1) -> List[int]:
    """
    Find all narcissistic numbers with `num_digits` digits.

    This is the preferred function to use when searching for narcissistic numbers of more than 5
    digits.

    Parameters
    ----------
    num_digits : integer
        The number of digits of the narcissistic numbers to find.
    processes : integer
        The number of processes over which to parallelize the workload.

    Returns
    -------
    list(integer)
        A list of all the narcissistic numbers with `num_digits` digits in increasing order.
    """
    pool = mp.Pool(processes)
    found: List[int] = []

    for chunk_start, chunk_end in p.get_chunk_indices(
        d.lowest_n_digit_number(num_digits), d.highest_n_digit_number(num_digits), processes):
        pool.apply_async(
            __get_narcissistic_for_chunk,
            args=(range(chunk_start, chunk_end), num_digits),
            callback=p.collect_result(found))

    pool.close()
    pool.join()

    return sorted(
        narcissistic_number for chunk_result in found for narcissistic_number in chunk_result)
