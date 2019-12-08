"""
Functions for number digit manipulation.
"""
import math
from typing import Generator


def is_single_digit(number: int) -> bool:
    """
    Determine if a number consists of just one digit.

    Parameters
    ----------
    number : integer
        The integer to check.

    Returns
    -------
    boolean
        True when `number` is a single digit, False otherwise.
    """
    return number // 10 in [0, -1] and number != -10


def digit_split(number: int) -> Generator[int, None, None]:
    """
    Split a number into its digits.

    Parameters
    ----------
    number : integer
        A positive integer.

    Returns
    -------
    generator(integer, None, None)
        A generator of the digits of `number`, ordered from left to right.
    """
    if is_single_digit(number):
        yield number
    else:
        for power in range(math.ceil(math.log(number, 10)) - 1, -1, -1):
            yield (number // (10 ** power)) % 10


def lowest_n_digit_number(num_digits: int) -> int:
    """
    Get the lowest number consisting of `num_digits`.

    Parameters
    ----------
    num_digits : integer
        The number of digits the result should have.

    Returns
    -------
    integer
        The lowest number with `num_digits` digits, in base 10.
    """
    if num_digits == 1:
        return 0

    return 10 ** (num_digits - 1)


def highest_n_digit_number(num_digits: int) -> int:
    """
    Get the highest number consisting of `num_digits`.

    Parameters
    ----------
    num_digits : integer
        The number of digits the result should have.

    Returns
    -------
    integer
        The highest number with `num_digits` digits, in base 10.
    """
    return 10 ** (num_digits) - 1
