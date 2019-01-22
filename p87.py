""" Problem 87

The smallest number expressible as the sum of a prime square, prime cube, and
prime fourth power is 28. In fact, there are exactly four numbers below fifty
that can be expressed in such a way:

    28 = 2**2 + 2**3 + 2**4
    33 = 3**2 + 2**3 + 2**4
    49 = 5**2 + 2**3 + 2**4
    47 = 2**2 + 3**3 + 2**4

How many numbers below fifty million can be expressed as the sum of a prime
square, prime cube, and prime fourth power?
"""

import utils.numtheory
import bisect

class PowerMemoizer(object):

    def __init__(self):
        self.d = {}

    def __call__(self, x, n):
        """ Computes x^n with memoization """
        if (x, n) not in self.d:
            self.d[(x,n)] = x**n
        return self.d[(x,n)]

power = PowerMemoizer()

def sums_below(N):
    N = int(N)
    largest_fourth = int(N**(1.0/4))+1
    largest_third = int(N**(1.0/3))+1
    largest_sqrt = int(N**(1.0/2))+1
    primes = list(utils.numtheory.bounded_soe(largest_sqrt))
    # Find the indicies of the next values greater than or equal to
    # largest_fourth, largest_third, and largest_sqrt in our list of
    # primes
    fourth_index = bisect.bisect_left(primes, largest_fourth)
    third_index = bisect.bisect_left(primes, largest_third)
    sqrt_index = bisect.bisect_left(primes, largest_sqrt)
    # Create a set of vals
    calculated_vals = set()
    for fourth in primes[:fourth_index+1]:
        s4 = power(fourth, 4)
        for third in primes[:third_index+1]:
            s3 = s4 + power(third, 3)
            if s3 >= N: break
            for sqrt in primes[:sqrt_index+1]:
                s = s3 + power(sqrt, 2)
                if s <= N:
                    calculated_vals.add(s)
                else:
                    break
    return len(calculated_vals)

def PROFILE():
    import cProfile
    cProfile.run('sums_below(5e7)')

if __name__ == '__main__':
    import utils
    #PROFILE()
    utils.solution_printer(sums_below, (5e7,))
