""" Problem 101

If we are presented with the first k terms of a sequence it is impossible to
say with certainty the value of the next term, as there are infinitely many
polynomial functions that can model the sequence.

As an example, let us consider the sequence of cube numbers. This is defined
by the generating function:
    u_n = n^3: 1, 8, 27, 64, 125, 216, ...

Suppose we were only given the first two terms of this sequence. Working on the
principle that "simple is best" we should assume a linear relationship and
predict the next term to be 15 (common difference 7). Even if we were presented
with the first three terms, by the same principle of simplicity, a quadratic
relationship should be assumed.

We shall define OP(k, n) to be the nth term of the optimum polynomial generating
fuction for the first k terms of a sequence. It should be clear that OP(k, n)
will acculrately generate the terms of the sequence of n<=k, and potentially
the first incorrect term (FIT) will be OP(k, k+1); in which case we shall call
it a bad OP (BOP).

As a basis, if we were only given the first term of a sequence, it would be most
sensible to assume constancy; that is, for n>=2, OP(1, n) = u_1.

Hence we obtain the following OPs for the cubic sequence:
                       
    OP(1, n)=1              1, 1, 1, 1, ...
                               ^
    OP(2, n) = 7n-6         1, 8, 15, ...
                                   ^
    OP(3, n) = 6n^2-11n+6   1, 8, 27, 58, ...
                                      ^
    OP(4, n) = n^3          1, 8, 27, 64, 125, ...

Clearly no BOPs exist for k>=4.

By considering the sum of FITs generated by the BOPs (indicated with carats
underneath in the above example) we obtain 1 + 15 + 58 = 74.

Consider the following tenth degree polynomial generating function:
    u_n = 1 - n + n^2 - n^3 + n^4 - n^5 + n^6 - n^7 + n^8 - n^9 + n^10

Find the sum of FITs for the BOPs.
"""

from euler.utils import memoize
from euler.utils import poly
from fractions import Fraction
import itertools

EXAMPLE_COEFFS = [0, 0, 0, 1]
PROBLEM_COEFFS = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1]


def lagrange(x_arr, y_arr):
    """ Returns the Lagrange interpolation polynomial for the set of k+1 data
    points (x0, y0), (x1, y1), ... (xk, yk) where no to xj are the same.
    
    L(x) := sum(yj*lj(x), j in [0, k]) where:
    lj(x) := pow((x-xm)/(xj-xm), 0<m<k and m!=j)"""
    assert len(x_arr) == len(y_arr)
    k = len(x_arr)
    L = poly.NullPoly
    for j in range(k):
        L = L + (y_arr[j] * _ell(x_arr, j))
    return L

def _ell(x_arr, j):
    k = len(x_arr)
    ans = poly.UnitPoly
    for m in range(k):
        if m == j: continue
        # A + Bx with A = -xm/(xj-xm) and B = 1/(xj-xm)
        A = Fraction(-x_arr[m], x_arr[j] - x_arr[m])
        B = Fraction(1, x_arr[j] - x_arr[m])
        ans = ans * poly.Poly([A, B])
    return ans
        

def sum_of_FITs(u_coeffs, x0=1):
    u_poly = poly.Poly(u_coeffs)
    BOP_limit = u_poly.degree + 1
    
    x_arr = [x0 + x for x in range(BOP_limit)]
    y_arr = [u_poly(x) for x in x_arr]

    ans = 0
    for k in range(1, len(x_arr)):
        # Get our Lagrange interpolating polynomial
        OP_k = lagrange(x_arr[:k], y_arr[:k])
        # Break out if our Lagrange interpolating poly equals our known one
        if OP_k.coeffs == u_poly.coeffs:
            continue
        # Else find the FIT (there must be one!)
        for n in itertools.count(k):
            if OP_k(n) != u_poly(n):
                ans+=OP_k(n)
                break
    return ans


if __name__ == '__main__':
    import euler.utils
    euler.utils.solution_printer(sum_of_FITs, (PROBLEM_COEFFS,))
