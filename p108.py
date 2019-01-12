""" Problem 108

In the following equation x, y and n are positive integers.

    1/x + 1/y = 1/n

For n=4 there are exactly three distinct solutions:

    1/5 + 1/20 = 1/4
    1/6 + 1/12 = 1/4
    1/8 + 1/8 = 1/4

What is the least value of n for which the number of distinct
solutions exceeds one-thousand?

NOTE: This problem is an easier version of problem 110; it is
strongly advised that you solve this one first.
"""

from __future__ import print_function
from euler.utils.numtheory import factorize
from itertools import count


def count_solutions(n):
    """ Counts integer solutions (x, y) to 1/x + 1/y = 1/n for integer n.

    Since we know x, y > n, let x=n+a, y=n+b, so we have:
        1/(n+a) + 1/(n+b) = 1/n
    Combining terms on the LHS gives:
        ((n+b) + (n+a))/((n+a)(n+b) = 1/n
        (2n+a+b)/(n^2+an+bn+ab) = 1/n
        2n^2 + an + bn = n^2 + an + bn + ab
        n^2 = ab
    So our number of solutions is the number of (a,b) which divide n^2

    Now n^2 has divisors d1, d2,..., d(i-1), n, d(i+1),..., dN
    and d1*dN=n^2, d2*d(N-1)=n^2, ..., d(i-1)*d(i+1)=n^2, n*n=n^2

    So if d(n) gives the number of divisors of n, we have:
        count_solutions(n) = (d(n^2)+1)/2

    If M has prime factorizations M=p1^e1 * p2^e2 * ... * pk^ek then:
        d(M) = prod(ei + 1, i in range(1, k))
    so d(M^2) = prod(2*ei + 1, i in range(1, k))
    """
    ans = 1
    for e in factorize(n).itervalues():
        ans *= (2*e + 1)
    ans = (ans+1)/2
    return ans


def min_n_with_at_least_N_solutions(N):
    """ Gives the lowest n which has at least N distinct pairs (x,y) solving
        1/x + 1/y = 1/n   (x < y)

    For debugging, prints each n which has more divisors than all m<n. """
    n_max, s_max = 0, 0
    for n in count(4):
        solutions = count_solutions(n)
        if solutions > s_max:
            n_max, s_max = n, solutions
            print('count_solutions({!s}) = {!s}'.format(n_max, s_max))
        if solutions > N:
            return n


if __name__ == '__main__':
    import euler.utils
    euler.utils.solution_printer(min_n_with_at_least_N_solutions, (1000,))
