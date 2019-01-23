""" Problem 88

A natural number, N, that can be written as the sum and product of a given set
of at least two natural numbers, {a_1, a_2, ..., a_k} is called a product-sum
number: N = a_1 + a_2 + ... + a_k = a_1 x a_2 x ... x a_k.

For example, 6 = 1 + 2 + 3 = 1 x 2 x 3

For a given set of size, k, we shall call the smallest N with this property a
minimal product-sum number. The minimal product-sum numbers for sets of size
k = 2, 3, 4, 5, and 6 are as follows:
    k=2: 4  = 2 x 2                 = 2 + 2
    k=3: 6  = 1 x 2 x 3             = 1 + 2 + 3
    k=4: 8  = 1 x 1 x 2 x 4         = 1 + 1 + 2 + 4
    k=5: 8  = 1 x 1 x 2 x 2 x 2     = 1 + 1 + 2 + 2 + 2
    k=6: 12 = 1 x 1 x 1 x 1 x 2 x 6 = 1 + 1 + 1 + 1 + 2 + 6

Hence for 2 <= k <= 6, the sum of all the minimal product-sum numbers is
4 + 6 + 8 + 12 = 30; note that 8 is only counted once in the sum.

In fact, as the complete set of minimal product-sum numbers for 2 <= k <= 12 is
{4, 6, 8, 12, 15, 16}, the sum is 61.

What is the sum of all the minimal product-sum numbers for 2 <= k <= 12000?
"""

import utils.numtheory
    
def min_product_sum_numbers(kmin, kmax):
    # List set of k-values that haven't had a minimal N associated with them
    # (for fast while-loop bail-out checking)
    elements_to_go = set(range(kmin, kmax+1))
    # Dict of k: (N, [a1, a2, ..., ak])
    N_mins = {}
    # We start with N=4 (but our while loop first increments by 1!)
    N = 3
    while elements_to_go:
        # Increment N:
        N+=1
        # A prime N will never be a minimal product-sum number for any k
        if utils.numtheory.isprime(N):
            continue
        # We get all the possible factorizations of N (up to rearrangement)
        for factors in utils.numtheory.all_factorizations(N):
            # The factorization N*1 can never work! Bail out of the
            # following calculations for this factorizations, and move
            # to the next factorization
            if len(factors) == 1:
                continue
            # Now compute the sum of the factorization.
            fact_sum = sum(factors)
            # Bail out if this sum is greater than N
            if fact_sum > N:
                continue
            # N minus fact_sum gives the number of 1's which must be added to
            # the factor sum to give N:
            # For N=12 and fact_sum=(3+2+2)=7, we calculate num_ones=12-7=5
            num_ones = N - fact_sum
            # So for our example, we need 5 1's to make the sum and product
            # equal 12.
            # 12 = 1+1+1+1+1+3+2+2 = 1*1*1*1*1*3*2*2
            # So in this case, k = len(1,1,1,1,1,3,2,2)
            #                    = num_ones + len(factors)
            k = num_ones + len(factors)
            # If this k is in our elements_to_go set, we know that this N is
            # the smallest product-sum number for that k. So update our answer
            # dict and remove k from our elements to go
            if k in elements_to_go:
                N_mins[k] = (N, factors+[1]*num_ones)
                elements_to_go.remove(k)
    return N_mins

def sum_of_minimal_product_sum_numbers(kmin, kmax):
    d = min_product_sum_numbers(kmin, kmax)
    vals = [v[0] for v in d.values()]
    return sum(set(vals))

def PROFILE():
    import cProfile
    cProfile.run('sum_of_minimal_product_sum_numbers(2, 5000)')

if __name__ == '__main__':
    import utils
    utils.solution_printer(sum_of_minimal_product_sum_numbers,
                                 (2, 12000))
