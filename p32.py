""" Problem 32

We shall say that an n-digit number is pandigital if it makes use of all the
digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1
through 5 pandigital.

The product 7254 is unusual, as the identity, 39 * 186 = 7254, containing 
multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity
can be written as a 1 through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only
include it once in your sum.
"""

import itertools
import operator
import functools

# ABCDEFGHI

def is_pandigital_product(a, b):
    return ''.join(sorted(str(a)+str(b)+str(a*b))) == '123456789'

def pandigital_candidates(number, candidate_size=1):
    """ Given a number, finds all k-permutations (k=candidate_size) of the
    digits 1-9 which exclude the digits in argument 'number' """
    pool = set('123456789')
    for digit in str(number):
        pool.discard(digit)
    pool = tuple(sorted(pool))
    for raw in itertools.permutations(pool, candidate_size):
        yield int(''.join(raw))

def digit_permutations(size=1):
    """ Gives all n-digit numbers with no duplicate digits
    >>> list(digit_permutations(1))
    (1, 2, 3, 4, ..., 9)
    >>> list(digit_permutations(2))
    (12, 13, ..., 19, 21, 23, ..., 29, ..., 96, 97, 98) """
    for raw in itertools.permutations('123456789', size):
        yield int(''.join(raw))

def a_b_pandigitals(a_oom, b_oom):
    """ Gives all pandigital triples (A, B, C) where A is of order-of-magnitude a_oom and
    B is of order-of-magnitude b_oom

    So a_b_pandigitals(2, 3) gives a list of all triples AB * CDE = FGHI. """
    answer = []
    for a in digit_permutations(a_oom):
        answer.extend((a, b, a*b) for b in pandigital_candidates(a, b_oom)
                      if is_pandigital_product(a, b))
    return answer

def ANSWER():
    # The only possible triples must be of forms:
    #   1) A * BCDE = FGHI
    #   2) AB * CDE = FGHI
    dirty_list = a_b_pandigitals(1, 4) + a_b_pandigitals(2, 3)
    # We need only sum unique products:
    products = set(triple[2] for triple in dirty_list)
    return functools.reduce(operator.add, products)

if __name__ == '__main__':
    import utils
    utils.solution_printer(ANSWER)
