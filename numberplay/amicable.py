from numberplay.utils import division as div
from numberplay.utils import digits as dig

def get_amicable(number):
    amicable_candidate = sum(div.find_proper_divisors(number))

    if  sum(div.find_proper_divisors(amicable_candidate)) == number:
        return amicable_candidate

    return None

def find_amicable_numbers(num_digits):

    amicable_tuples = []

    for number in range(
        dig.lowest_n_digit_number(num_digits), dig.highest_n_digit_number(num_digits) + 1):

        amicable = get_amicable(number)

        if amicable is not None:
            amicable_tuples.append((number, amicable))

    return amicable_tuples
