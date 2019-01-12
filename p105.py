""" Problem 105

Let S(A) represent the sum of elements in set A of size n. We shall call it a
special sum set if for any two non-empty disjoint subsets, B and C, the
following properties are true:

    i. S(B) != S(C); that is, the sums of the subsets cannot be equal.
   ii. If B contains more elements than C, then S(B) > S(C)

For example, {81, 88, 75, 42, 87, 84, 86, 65} is not a special sum set because
65+87+88 = 75+81+84, whereas {157, 150, 164, 119, 79, 159, 161, 139, 158}
satisfies both rules for all possible subset pair combinations and S(A) = 1286.

Using `sets.txt`, a 4K text file with one-hundred sets containing seven to
twelve elements (the two examples given above are the first two sets in the
file), identify all the special sum sets, A1, A2,...,Ak and find the value of
S(A1)+S(A2)+...+S(Ak)

NOTE: This problem is related to problems 103 and 106.
"""

from itertools import imap, combinations
from math import ceil

def load_sets():
    print 'Opening sets.txt'
    with open('sets.txt') as f:
        for line in f:
            yield list(map(int, line.split(',')))
    print 'Closing sets.txt'


def is_special(iterable):
    """ Returns True if iterable is a special sum set.

    First checks property ii by enumerating all sets B, C where len(B)=len(C)+1,
    B is composed of the first r elements of sorted(iterable), and C is composed
    of the last r-1 elements of sorted(iterable).

    So now we know that for each B, C with len(B)>len(C), sum(B)>sum(C). So to
    check property i, we just check that for all sets B, C where
    len(B)==len(C), sum(B)!=sum(C). """
    A = list(sorted(iterable))
    n = len(A)
    # Check property ii for sets constructed from "end slices" with B being the
    # slice from the beginning of length r and C being the slice from the
    # end of length r-1.
    for r in range(2, n-int(n/2)+1):
        B, C = A[:r], A[1-r:]
        if sum(B) <= sum(C):
            return False
    # Check property i. For each r in 2...floor(len(iterable)/2), we construct
    # all all subsets of length r. We collect the sum in a set and check that
    # we get no duplicate sums.
    #
    # Note that we don't have to check that sets with duplicate sums are
    # disjoint. Indeed, note first that we never generate the same set twice.
    # Then note that if non-disjoint sets B, C exist such that sum(B)==sum(C)
    # and len(B)==len(C), we can collect the common elements to both in a set
    # J (=B&C where '&' means 'intersection'). So
    #     B = (B-J)|J and
    #     C = (C-J)|J        NOTE: '|' means 'union', '-' means 'difference'
    # So (B-J) and (C-J) are disjoint, and both are disjoint to J. So
    #     sum(B-J)+sum(J) = sum(B) == sum(C) = sum(C-J)+sum(J)
    # So we still have sets B'=B-J and C'=C-J with sum(B')==sum(C') and
    # len(B')==len(C')
    for r in range(2, int(n/2)+1):
        sums = set()
        for B in combinations(A, r):
            sB = sum(B)
            if sB in sums:
                return False
            sums.add(sB)
    return True
            
    
#def is_special(iterable):
#    """ Returns True if for any two disjoin subsets B, C of `iterable`
#    satisfy the following properties:
#
#        i. S(B) != S(C); that is, the sums of the subsets cannot be equal.
#       ii. If B contains more elements than C, then S(B) > S(C)
#    """
#    for B, C in disjoint_subsets(iterable):
#        SB, SC = sum(B), sum(C)
#        lB, lC = len(B), len(C)
#        # Condition i
#        if SB == SC:
#            return False
#        # Condition ii
#        if SB < SC and lC < lB: return False
#        if SC < SB and lB < lC: return False 
#    return True


def ANSWER():
    special_sets = filter(is_special, load_sets())
    return sum(sum(s) for s in special_sets)


if __name__ == '__main__':
    import euler.utils
    euler.utils.solution_printer(ANSWER)

