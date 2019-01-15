""" Problem 37

The number 3797 has an interesting property. Being prime itself, it is possible
to continuously remove digits from left to right, and remain prime at each
stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797,
379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to
right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
"""

import math
import operator
import functools

def trial_division_candidates(number):
    """ Creates a list of candidate divisors for a given number.
    For use with is_prime() trial division algo. """
    r = math.sqrt(number)
    P = int((r-1.0)/6) + 1
    M = int((r+1.0)/6) + 1
    return ([2, 3] + [6*p+1 for p in range(1, P)] +
            [6*m-1 for m in range(1, M)])

def is_prime(n):
    """ Simple trial-division primality test with a few optimizations """
    if n == 1 or n == 0:
        return False
    if n == 3 or n == 2:
        return True
    composite = any(n % factor == 0 for factor in trial_division_candidates(n))
    return not composite

def right_truncatable_primes():
    """ Creates a list of right-truncatable primes. Basically, given a list
    of n-digit right truncatable primes, we construct the next generation by:
        1. For each prime in the current generation, construct 4 new (n+1)-digit
           candidate primes by appending 1, 3, 7, or 9 to the end.
        2. Mash all the (n+1)-digit candidates derived from step 1 into a big
           list. Test each one for primality
        3. Test each candidate in the list from step 2 for primality. This is
           your next generation.
    It turns out that there is a finite number of such primes, so the above
    algorithm terminates. """
    curr_gen = next_gen = answer = [2, 3, 5, 7]
    while next_gen:
        next_gen = []
        for prime in curr_gen:
            p = str(prime)
            candidates = map(int, [p+'1', p+'3', p+'7', p+'9'])
            next_gen.extend(filter(is_prime, candidates))
        answer.extend(next_gen)
        curr_gen = next_gen
    return answer

def is_left_truncatable_prime(n):
    left_substrings = [str(n)[i:] for i in range(len(str(n)))]
    return all(is_prime(int(substring)) for substring in left_substrings)

def ANSWER():
    right_trunc_primes = right_truncatable_primes()
    truncatable_primes = filter(is_left_truncatable_prime, right_trunc_primes)
    euler_trunc_primes = list(filter(lambda x: x>9, truncatable_primes))
    assert len(euler_trunc_primes) == 11
    return functools.reduce(operator.add, euler_trunc_primes)

if __name__ == '__main__':
    import utils
    utils.solution_printer(ANSWER)
