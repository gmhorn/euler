""" Problem 106

Let S(A) represent the sum of elements in set A of size n. We shall call it a
special sum set if for any two non-empty disjoint subsets, B and C, the
following properties are true:

    i. S(B) != S(C); that is, the sums of the subsets cannot be equal.
   ii. If B contains more elements than C, then S(B) > S(C)

For this problem we shall assume that a given set contains n strictly
increasing elements and it already satisfies the second rule.

Surprisingly, out of the 25 possible subset pairs that can be obtained from a
set for which n=4, only 1 of these pairs need to be tested for equality (first
rule). Similarly, when n=7, only 70 out of the 966 subset pairs need to be
tested.

For n=12, how many of the 261625 subset pairs that can be obtained need to be
tested for equality?

NOTE: This problem is related to problems 103 and 105.
"""

from itertools import imap, combinations, groupby
from euler.utils import nCr

def property_one_candidates(n):
    """ To test for property i given that we know property ii is true, use this
    function to generate pairs of index masks.

    So if your set is A = [a, b, c, d], and this function returns ([1,4], [2,3])
    then you should check if sum([a, d]) == sum([b, c]).

    Works based on the assumption that, given a sorted A, we do not need to
    check equal-sized sets B and C whose elements are (index-wise) alternatingly
    always greater in one than the other.

    So for example, comparing indicies [1, 2, 5] and [3, 4, 6] is unncessary
    because A[1] < A[3], A[2] < A[4] and A[5] < A[6], so sum([A[1], A[2], A[5]])
    will obviously be less than sum([A[3], A[4], A[6]])
    """
    A = list(range(n))
    
    # Create all subsets of length r for r between 2 and half of n (inclusive)
    for r in range(2, int(n/2)+1):
        all_subsets = [X for X in combinations(A, r)]
        # Then for each pair, test out of they meet our "closeness" criteria
        for B, C in combinations(all_subsets, 2):
            # Break out of this cycle if B and C are not disjoint
            if set(B) & set(C): continue
            # If the tally of B[i]<C[i] is between [-1, 1], we yield the sets
            tally = 0
            for b, c in zip(B, C):
                if b < c: tally-=1
                else: tally+=1
            if abs(tally)<r:
                yield B, C

def num_candidates(n):
    tally = 0
    for B, C in property_one_candidates(n):
        tally+=1
    return tally

if __name__ == '__main__':
    import euler.utils
    euler.utils.solution_printer(num_candidates, (12,))
