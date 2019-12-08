"""
Tests for numberplay.narcissistic.
"""
import unittest

from numberplay import narcissistic as tst


class TestIsNarcissistic(unittest.TestCase):
    """
    A test fixture for:
        numberplay.narcissistic.is_narcissistic
    """

    # pylint:disable=missing-docstring
    @classmethod
    def setUpClass(cls):
        cls.single_digits = range(10)
        cls.double_digits = range(10, 100)
        cls.three_digit_narcissistic = {153, 370, 371, 407}
        cls.four_digit_narcissistic = {1634, 8208, 9474}

        cls.largest_narcissistic = {
            1219167219625434121569735803609966019,
            12815792078366059955099770545296129367,
            115132219018763992565095597973971522400,
            115132219018763992565095597973971522401}

        cls.three_digit_nonnarcissistic = [
            number for number in range(100, 1000) if number not in cls.three_digit_narcissistic]

        cls.four_digit_nonnarcissistic = [
            number for number in range(1000, 10000) if number not in cls.four_digit_narcissistic]

    def test_single_digits_are_narcissistic(self):
        for number in self.single_digits:
            self.assertTrue(tst.is_narcissistic(number))

    def test_double_digits_are_not_narcissistic(self):
        for number in self.double_digits:
            self.assertFalse(tst.is_narcissistic(number))

    def test_3_narcissistic_are_narcissistic(self):
        for number in self.three_digit_narcissistic:
            self.assertTrue(tst.is_narcissistic(number))

    def test_4_narcissistic_are_narcissistic(self):
        for number in self.four_digit_narcissistic:
            self.assertTrue(tst.is_narcissistic(number))

    def test_largest_narcissistic_are_narcissistic(self):
        for number in self.largest_narcissistic:
            self.assertTrue(tst.is_narcissistic(number))

    def test_3_digit_nonnarcissistic_are_not_narcissistic(self):
        for number in self.three_digit_nonnarcissistic:
            self.assertFalse(tst.is_narcissistic(number))

    def test_4_digit_nonnarcissistic_are_not_narcissistic(self):
        for number in self.four_digit_nonnarcissistic:
            self.assertFalse(tst.is_narcissistic(number))
    # pylint:enable=missing-docstring


if __name__ == '__main__':
    unittest.main(verbosity=2)
