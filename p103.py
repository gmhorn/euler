""" Problem 103

Let S(A) represent the sum of elements in set A of size n. We shall call it a
special sum set if for any two non-empty disjoint subsets, B and C, the
following properties are true:

    i. S(B) != S(C); that is, the sums of the subsets cannot be equal.
   ii. If B contains more elements than C, then S(B) > S(C)

If S(A) is minimized for a given n, we shall call it an optimum special sum set.
The first five optimum special sum sets are given below.

    n=1:  {1}
    n=2:  {1, 2}
    n=3:  {2, 3, 4}
    n=4:  {3, 5, 6, 7}
    n=5:  {6, 9, 11, 12, 13}

It _seems_ that for a given optimum set, A={a1, a2,...,an}, the next optimum set
is of the form B={b, a1+b, a2+b,...,an+b} where b is the "middle" element in
the previous row.

By applying this "rule" we would expect the optimum set for n=6 to be:

    n=6:  {11, 17, 20, 22, 23, 24)

with S(A)=117. However, this is not the optimum set. The optimum set for n=6 is:

    n=6:  {11, 18, 19, 20, 22, 25}

with S(A)=115 and the corresponding set string: 111819202225.

Given that A is an optimum special sum st for n=7, find its set string.

NOTE: This problem is related to problems 105 and 106.
"""

from itertools import combinations, product, ifilter

N1 = [1]
N2 = [1, 2]
N3 = [2, 3, 4]
N4 = [3, 5, 6, 7]
N5 = [6, 9, 11, 12, 13]
N6 = [11, 18 ,19, 20, 22, 25]
N6_Naive = [11, 17, 20, 22, 23, 24]

def TEST():
    print 

def next_minimal(last_gen, p_min, p_max):
    # Generate candidate and assert it's good
    last_gen = list(sorted(last_gen))
    b = last_gen[int(len(last_gen)/2)]
    candidate = list(sorted([b] + [ai+b for ai in last_gen]))
    assert len(candidate) == len(last_gen)+1
    assert is_special(candidate)
    candidate_sum = sum(candidate)

    permutation_vectors = product(range(p_min, p_max), repeat=len(candidate))
    for permutation_vector in ifilter(lambda x: sum(x)<0, permutation_vectors):
        new_candidate = [a-p for a,p in zip(candidate, permutation_vector)]
        if sum(new_candidate) < candidate_sum and is_special(new_candidate):
            candidate = new_candidate
            candidate_sum = sum(new_candidate)
    return candidate
    

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

def ANSWER():
    return ''.join(map(str, next_minimal(N6, -3, 3)))

if __name__ == '__main__':
    import euler.utils
    euler.utils.solution_printer(ANSWER)
