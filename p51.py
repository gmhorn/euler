""" Problem 51

By replacing the 1st digit of *3, it turns out that six of the nine possible
values: 13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit
number is the first example having seven primes among the ten generated numbers,
yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993.
Consequently 56003, being the first member of this family, is the smallest
prime with this property.

Find the smallest prime which, by replacing part of the number (not necessarily
adjacent digits) with the same digit, is part of an eight prime value family.
"""

from __future__ import print_function
import itertools
import euler.utils.numtheory


def generate_candidates():
    """ Speculate that the candidates will be 6 digits and 3 repeats.
    Find all 6-digit primes with 3 repeats.

    Also, since we're looking for 8 replacements, 0 1 or 2 must be repeated.

    Also, the last digit cannot be one of the ones ultimately replaced, so we
    consider only the first elements. """
    prime_list = euler.utils.numtheory.bounded_soe(999999, 100000)
    def candidate_filter(n):
        s = str(n)[:-1]
        return (s.count('0') == 3) or (s.count('1') == 3) or (s.count('2') == 3)
    return filter(candidate_filter, prime_list)

def replacement_family(num, replace_digit):
    """ Given a starting number, and a digit to replace, returns a list of
    numbers where the first three instances of the replacement digit have been
    substituted.

    >>> replacement_family(123220, 2)
    [123220, 133330, 143440, 153550, 163660, 173770, 183880, 193990]
    >>> replacement_family(921116, 1)
    [921116, 922226, 923336, 924446, 925556, 926666, 927776, 928886, 929996]
    """
    replace_digit, num = str(replace_digit), str(num)
    all_digits = '0123456789'
    digits = all_digits[all_digits.find(replace_digit):]
    replacements = map(lambda x: num.replace(replace_digit, x, 3), digits)
    return map(int, replacements)

def ANSWER():
    candidates = generate_candidates()
    primes = list(euler.utils.numtheory.bounded_soe(999999, 100000))
    for candidate in candidates:
        candidate_minus_last_digit = str(candidate)[:-1]
        if candidate_minus_last_digit.count('0') == 3:
            family = replacement_family(candidate, 0)
        elif candidate_minus_last_digit.count('1') == 3:
            family = replacement_family(candidate, 1)
        else:
            family = replacement_family(candidate, 2)
        prime_family = list(filter(lambda x: x in primes, family))
        if len(prime_family) == 8:
            print('Prime family: ', prime_family)
            return prime_family[0]
    return -1

if __name__ == '__main__':
    import euler.utils
    euler.utils.solution_printer(ANSWER)
