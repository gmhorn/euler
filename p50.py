""" Problem 50

The prime 41, can be written as the sum of six consecutive primes:
    41 = 2 + 3 + 5 + 7 + 11 + 13

This is the longest sum of consecutive primes below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime,
contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most
consecutive primes?
"""

from __future__ import print_function

import itertools
import math
import euler.utils.numtheory

def summand_upper_bound(x):
    """ Sums all the primes, starting with 2, until the sum is greater than
    or equal to x. Then it returns the number of primes summed.

    Consider calculating summand_upper_bound(110). Since:
        100 = 2 + 3 + 5 + 7 + 11 + 13 + 17 + 19 + 23
        129 = 2 + 3 + 5 + 7 + 11 + 13 + 17 + 19 + 23 + 29
    we return the value len([2, 3, 5, 7, 11, 13, 17, 19, 23, 29]) == 10.
    """
    N, c = 0, 0
    primes = euler.utils.numtheory.soe()
    while c < x:
        c += next(primes)
        N += 1
    return N
    

def longest_consecutive_prime_sum_less_than(x):
    """ Find the summands of the largest conescutive prime sum below x """
    # 1. To find the longest consecutive prime sum less than x, we first give
    # an upper bound on the length of any sum of primes below x. That upper
    # bound is the number of consecutive primes, starting with 2, that can be
    # summed to give the maximal (not-necessarily prime) number below x.
    n = summand_upper_bound(x)
    # 2. Now create a list of all primes up to x (could be optimized to a
    # smaller list if performance starts degrading for large x).
    primes = list(euler.utils.numtheory.bounded_soe(x))
    N = len(primes)
    # 3. Now we find the solution. Our algorithm terminates when we find the
    # first slice of the prime list whose elements sum to a prime less than x.
    #
    # Consider a list of primes:
    #     2  3  5  7  11  13  ...  p_h  p_i  p_j  p_k  ...  p_x
    # Start by taking n-length slices of this list, where n is initially our
    # upper bound for our summand. Take the n-length slices from the beginning
    # of the prime list
    #    [2  3  5  7  11  13  ...  p_h  p_i  p_j] p_k  ...  p_x
    # Take the sum and, if it's not prime, take the n-length slice starting from
    # the second element.
    #     2 [3  5  7  11  13  ...  p_h  p_i  p_j  p_k] ...  p_x
    # If this slice sums to a number greater than x, we've exhausted all the
    # choices of n-length slices of consecutive primes who sum to below x.
    #
    # So start taking (n-1)-length slices of the prime list, starting at the
    # beginning
    #    [2  3  5  7  11  13  ...  p_h  p_i] p_j  p_k  ...  p_x
    # And keep "sliding" the slice down until the sum either exceeds x or is
    # prime. If it exceeds x, decrement our slice length and start from the
    # beginning of the prime list.
    #     2 [3  5  7  11  13  ...  p_h  p_i  p_j] p_k  ...  p_x  -- Not prime
    #     2  3 [5  7  11  13  ...  p_h  p_i  p_j  p_k] ...  p_x  -- >=x, decrement
    #    [2  3  5  7  11  13  ...  p_h] p_i  p_j  p_k  ...  p_x  -- Not prime
    #     2 [3  5  7  11  13  ...  p_h  p_i] p_j  p_k  ...  p_x  -- PRIME. done
    for consec_nums in range(n, 2, -1):
        for i in range(0, N-(consec_nums-1)):
            vals = primes[i:i+consec_nums]
            a = sum(vals)
            if a > x:
                break
            if a in primes:
                return vals
    return None

def TEST():
    import unittest
    
    class _TEST(unittest.TestCase):

        def test_100_seq(self):
            expect = [2, 3, 5, 7, 11, 13]
            actual = longest_consecutive_prime_sum_less_than(100)
            self.assertEqual(actual, expect)

        def test_1000_seq_len(self):
            expect = 21
            actual = len(longest_consecutive_prime_sum_less_than(1000))
            self.assertEqual(actual, expect)

        def test_1000_sum(self):
            expect = 953
            actual = sum(longest_consecutive_prime_sum_less_than(1000))
            self.assertEqual(actual, expect)
            
    suite = unittest.TestLoader().loadTestsFromTestCase(_TEST)
    unittest.TextTestRunner(verbosity=2).run(suite)

def PROFILE():
    import cProfile
    cProfile.run('ANSWER()')

def ANSWER():
    seq = longest_consecutive_prime_sum_less_than(1000000)
    ans = sum(seq)
    print('%i = %s + ... + %s' % (ans, ' + '.join(map(str, seq[:4])),
                                  ' + '.join(map(str, seq[-4:]))))
    print('%i consecutive primes from %i to %i' % (len(seq), seq[0], seq[-1]))
    return sum(longest_consecutive_prime_sum_less_than(1000000))

if __name__ == '__main__':
    import euler.utils
    euler.utils.solution_printer(ANSWER)
