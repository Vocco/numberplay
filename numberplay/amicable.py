"""
Functions to find amicable numbers.
"""
from typing import List, Optional, Tuple

from numberplay.utils import digits as dig
from numberplay.utils import division as div


def get_amicable(number: int) -> Optional[int]:
    """
    Get an amicable counterpart to a number.

    Parameters
    ----------
    number : integer
        The positive integer whose amicable counterpart to find.

    Returns
    -------
    integer | None
        The amicable counterpart to `number` if it exists, None otherwise.
    """
    amicable_candidate = sum(div.find_proper_divisors(number))

    if  sum(div.find_proper_divisors(amicable_candidate)) == number:
        return amicable_candidate

    return None

def find_amicable_numbers(num_digits: int) -> List[Tuple[int, int]]:
    """
    Find all amicable pairs of `num_digits` digits.

    Parameters
    ----------
    num_digits : integer
        The number of digits of the numbers in the amicable pairs to find.

    Returns
    -------
    list(tuple(integer, integer))
        A list of all amicable pairs of `num_digits` digits.
    """
    amicable_tuples = []

    for number in range(
            dig.lowest_n_digit_number(num_digits), dig.highest_n_digit_number(num_digits) + 1):

        amicable = get_amicable(number)

        if amicable is not None:
            amicable_tuples.append((number, amicable))

    return amicable_tuples
