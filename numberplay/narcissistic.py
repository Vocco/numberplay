"""
Functions to find narcissistic numbers.

An 'n-narcissistic number' is an n-digit number that is the sum of the n-th powers of its digits.
Other names include 'Armstrong numbers', 'perfect digital invariant', and 'plus perfect number'
"""
import functools as ft
import multiprocessing as mp
from typing import Iterable, List

from numberplay.utils import common as c
from numberplay.utils import digits as d
from numberplay.utils import parallel as p


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
    return list(filter(lambda number: is_narcissistic(number, num_digits), chunk))


def __highest_possible_n_narcissistic_sum(num_digits: int) -> int:
    """
    Return the highest possible narcissistic sum (sum of squared digits) for `num_digits` digits.

    The highest possible narcissistic sum of an n-digit number is 9^n + 9^n + ... 9^n, where the
    term repeats n times (once for each digit).

    Parameters
    ----------
    num_digits : integer
        The number of digits for which to find the highest possible narcissistic sum.

    Returns
    -------
    integer
        The highest possible narcissistic sum a number of `num_digits` digits could have.
    """
    return num_digits * (9 ** num_digits)


def is_narcissistic(number: int, num_digits=None) -> bool:
    """
    Determine whether a number is narcissistic.

    Parameters
    ----------
    number : integer
        A positive integer.
    num_digits : integer (optional)
        The number of digits of `number`. If not present, the number of digits will be computed.
        For batch processing of many numbers with the same number of digits, it is recommended to
        provide this value as means of optimization.

    Returns
    -------
    boolean
        True when `number` is narcissistic, False otherwise.
    """
    if num_digits is None:
        num_digits = len(list(d.digit_split(number)))

    return number == ft.reduce(
        lambda current_sum, digit: current_sum + digit ** num_digits, d.digit_split(number), 0)


def find_narcissistic_between(lowest: int, highest: int, num_processes=1) -> List[int]:
    """
    Find all narcissistic numbers between `lowest` and `highest`.

    Parameters
    ----------
    lowest : integer
        The lowest bound to consider. Positive integer.
    highest : integer
        The highest bound to consider. Positive integer.
    num_processes : integer
        The number of processes over which to parallelize the workload. It is highly recommended to
        utilize more processes when searching for narcissistic numbers of more than 5 digits, as
        the space to search is grows exponentially with respect to this value. Defaults to 1.

    Returns
    -------
    list(integer)
        An list over all the narcissistic numbers between `lowest` and `highest` in increasing
        order.
    """
    pool = mp.Pool(num_processes)
    num_digits_lower = len(list(d.digit_split(lowest)))
    num_digits_higher = len(list(d.digit_split(highest)))

    found: List[int] = []

    for digit_difference in range(num_digits_higher - num_digits_lower + 1):
        num_digits = num_digits_lower + digit_difference

        if not may_contain_narcissistic(num_digits):
            break

        digit_range_start = max(lowest, d.lowest_n_digit_number(num_digits))
        digit_range_end = min(highest, d.highest_n_digit_number(num_digits))

        for indices in p.get_chunk_indices(digit_range_start, digit_range_end, num_processes):
            pool.apply_async(
                __get_narcissistic_for_chunk,
                args=(range(*indices), num_digits),
                callback=p.collect_result(found))

    pool.close()
    pool.join()

    return sorted(c.flatten(found))


def may_contain_narcissistic(num_digits: int) -> bool:
    """
    Determine whether there might exist any narcissistic number of `num_digits` digits.

    Parameters
    ----------
    num_digits : integer
        The number of digits to check.

    Return
    ------
    boolean
        True if it is concievable that there may exist a narcissistic number of `num_digits`
        digits, False if such a number definitely cannot exist.
    """
    return __highest_possible_n_narcissistic_sum(num_digits) >= d.lowest_n_digit_number(num_digits)


def find_n_narcissistic(num_digits: int, num_processes=1) -> List[int]:
    """
    Find all narcissistic numbers with `num_digits` digits.

    Parameters
    ----------
    num_digits : integer
        The number of digits of the narcissistic numbers to find.
    num_processes : integer
        The number of processes over which to parallelize the workload. It is highly recommended to
        utilize more processes when searching for narcissistic numbers of more than 5 digits, as
        the space to search is grows exponentially with respect to the parameter. Defaults to 1.

    Returns
    -------
    list(integer)
        A list of all the narcissistic numbers with `num_digits` digits in increasing order.
    """
    return find_narcissistic_between(
        d.lowest_n_digit_number(num_digits), d.highest_n_digit_number(num_digits), num_processes)
