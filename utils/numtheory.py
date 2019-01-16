import itertools
import math
import bisect
import collections
import utils.contfrac
import utils

def soe():
    """ Generator version of the Sieve of Eratosthenes.

    Optimization does not record a prime's info in the dict until
    its square is seen among the candidates. This brings the space
    complexity below O(sqrt(n)) instead of O(n), for n primes produced.

    Created by Will Ness (http://stackoverflow.com/a/10733621)
    See also http://www.haskell.org/haskellwiki/Prime_numbers#From_Squares """
    #def add(D, x, s):
    #    while x in D: x+= s
    #    D[x] = s
    yield 2; yield 3; yield 5; yield 7;
    D = {}
    ps = (p for p in soe())
    p = next(ps) and next(ps)
    q = p*p
    for c in itertools.islice(itertools.count(9), 0, None, 2):
        if c not in D:
            if c < q: yield c
            else:
                x, s = c+2*p, 2*p
                while x in D: x += s
                D[x] = s
                p = next(ps)
                q = p*p
        else:
            s = D.pop(c)
            x = c+s
            while x in D: x += s
            D[x] = s

def bounded_soe(maximum=None, minimum=2):
    """ Generator version of the Sieve of Eartosthenes which starts above
    minimum and terminates when all primes below maximum are enumerated.

    A value of None for maximum corresponds to infinity, conceptually, as
    the upper bound. """
    if not maximum:
        for p in soe():
            if p >= minimum: yield p
    else:
        assert maximum > minimum
        ps = (p for p in soe())
        p = next(ps)
        while p <= maximum:
            if p >= minimum: yield p
            p = next(ps)


def allprimes():
    """ Generates all the prime numbers in sequence. Generator version of the
    Sieve of Eratosthenes.

    Optimization does not record a prime's info in the dict until
    its square is seen among the candidates. This brings the space
    complexity below O(sqrt(n)) instead of O(n), for n primes produced.

    Created by Will Ness (http://stackoverflow.com/a/10733621)
    See also http://www.haskell.org/haskellwiki/Prime_numbers#From_Squares """
    yield 2; yield 3; yield 5; yield 7;
    D = {}
    ps = (p for p in allprimes())
    p = next(ps) and next(ps)
    q = p*p
    for c in itertools.islice(itertools.count(9), 0, None, 2):
        if c not in D:
            if c < q: yield c
            else:
                x, s = c+2*p, 2*p
                while x in D: x += s
                D[x] = s
                p = next(ps)
                q = p*p
        else:
            s = D.pop(c)
            x = c+s
            while x in D: x += s
            D[x] = s

# Number of primes to add to _PRIMELIST_CACHE when we add more
_PRIMELIST_INCREMENT = 1000
_PRIMELIST_GEN = allprimes()
_PRIMELIST_CACHE = [next(_PRIMELIST_GEN) for i in range(_PRIMELIST_INCREMENT)]

def _extend_primelist_if_needed(b):
    """ Extends _PRIMELIST_CACHE to ensure we have primes up to b """
    while _PRIMELIST_CACHE[-1] < b:
        _PRIMELIST_CACHE.extend(next(_PRIMELIST_GEN)for i in
                                range(_PRIMELIST_INCREMENT))

def primelist(a, b):
    """ Return all primes in the range [a, b]

    >>> primelist(2, 15)
    [2, 3, 5, 7, 11, 13]
    >>> primelist(2, 13)
    [2, 3, 5, 7, 11, 13]
    >>> primelist(5, 13)
    [5, 7, 11, 13]
    >>> primelist(6, 13)
    [7, 11, 13] """
    #from math import ceil
    #from bisect import bisect_left, bisect_right
    a = max(2, int(math.ceil(a)))
    b = int(math.ceil(b))
    #while _PRIMELIST_CACHE[-1] < b:
    #    _PRIMELIST_CACHE.extend(next(_PRIMELIST_GEN) for i in range(1000))
    _extend_primelist_if_needed(b)
    a_index = bisect.bisect_left(_PRIMELIST_CACHE, a)
    b_index = bisect.bisect_right(_PRIMELIST_CACHE, b)
    return _PRIMELIST_CACHE[a_index:b_index]

def isprime(n):
    """ Tests if a number is prime using sieving.

    Not appropriate for very large n, because will generate all primes
    less than n (at least). """
    _extend_primelist_if_needed(n)
    i = bisect.bisect_left(_PRIMELIST_CACHE, n)
    return _PRIMELIST_CACHE[i] == n

def trial_division(n):
    """ Returns the integer factorization of n:
        n = p_1^e_1 * p_2^e_2 * p_m^e_m
    as a dict the keys are the p_i and the values are the e_i.

    Uses trial division to perform this factorization.

    So 100 = 2^2 * 5^2:
    >>> trial_division(100)
    {2: 2, 5: 2}

    And 10054323 = 31 * 36037 * 3^2:
    >>> trial_division(10054323)
    {3: 2, 36037: 1, 31: 1}
    """
    from collections import defaultdict
    prime_factors = defaultdict(int)
    for p in primelist(2, int(n**0.5)+1):
        if p*p > n: break
        while n % p == 0:
            prime_factors[p] += 1
            n /= p
    if n > 1:
        prime_factors[n] += 1
    return dict(prime_factors)


def factorize(n):
    """ Returns the integer factorization of n:
        n = p_1^e_1 * p_2^e_2 * p_m^e_m
    as a dict the keys are the p_i and the values are the e_i.

    So 100 = 2^2 * 5^2:
    >>> factorize(100)
    {2: 2, 5: 2}

    And 10054323 = 31 * 36037 * 3^2:
    >>> factorize(10054323)
    {3: 2, 36037: 1, 31: 1}

    As of now it simply uses trial_division. Later refinements might be to
    use other algorithms.
    """
    return trial_division(n)

@utils.memoize
def divisors(n):
    """ Returns a list of divisors of n.
    See: http://stackoverflow.com/a/1010463

    The divisors are ordered least to greatest. So 1 is always the first
    element.
    >>> divisors(24)
    [1, 2, 3, 4, 6, 8, 12, 24]
    >>> divisors(100)
    [1, 2, 4, 5, 10, 20, 25, 50, 100]
    
    Prime numbers will only have 1 and the itself as a divisor:
    >>> divisors(97)
    [1, 97]

    And 1 only has itself as a divisor:
    >>> divisors(1)
    [1]
    """
    divs = [1]
    f_dict = factorize(n)
    for factor, count in f_dict.iteritems():
        newdivs = divs
        for ignore in range(count):
            newdivs = map(lambda d: d*factor, newdivs)
            divs += newdivs
    return sorted(divs)

def num_of_divisors(n):
    """ Gives number of divisors of n. Equivalent to Mathematica's
    DivisorSigma[0, n]. """
    ans = 1
    for e in factorize(n).itervalues():
        ans *= (e+1)
    return ans

def sum_of_divisors(n):
    """ Gives the sum of the divisors of n. Equivalent to Mathematica's
    DivisorsSigma[1, n]. """
    num = 1
    denom = 1
    for p, e in factorize(n).iteritems():
        num *= ((p**(e+1)) - 1)
        denom *= (p-1)
    return num/denom

def partitions(n):
    """ Yields partitions of n in ascending order.
    See: http://homepages.ed.ac.uk/jkellehe/partitions.php

    Because the distinct partitions of a number grows very quickly as n
    increases, this is actuall a generator function:
    >>> p = partitions(5)
    >>> next(p)
    [1, 1, 1, 1, 1]
    >>> next(p)
    [1, 1, 1, 2]
    >>> next(p)
    [1, 1, 3]
    >>> next(p)
    [1, 2, 2]

    However, for small numbers, listing them all should be okay.
    >>> list(partitions(4))
    [[1, 1, 1, 1], [1, 1, 2], [1, 3], [2, 2], [4]]
    >>> list(partitions(5))
    [[1, 1, 1, 1, 1], [1, 1, 1, 2], [1, 1, 3], [1, 2, 2], [1, 4], [2, 3], [5]]

    Note that for any n, the first partition will be a list of n 1's, and the
    last will be the list [n]."""
    a = [0 for i in range(n+1)]
    k = 1
    a[0] = 0
    a[1] = n
    while k != 0:
        x = a[k-1] + 1
        y = a[k] - 1
        k = k-1
        while x <= y:
            a[k] = x
            y = y-x
            k = k+1
        a[k] = x+y
        yield a[:k+1]


def ordered_factorizations(n):
    """ Yields ordered factorizations of n.
    See: http://www.math.wvu.edu/~mays/Papers/Factorizations.pdf

    Because there can be many ordered factorizations, this is implemented
    as a generator function:
    >>> ords = ordered_factorizations(12)
    >>> next(ords)
    [2, 2, 3]
    >>> next(ords)
    [2, 3, 2]
    >>> next(ords)
    [2, 6]

    But for small numbers, listing them all should be okay:
    >>> list(ordered_factorizations(12))
    [[2, 2, 3], [2, 3, 2], [2, 6], [3, 2, 2], [3, 4], [4, 3], [6, 2], [12]]
    """
    if n == 1: yield []
    for d in divisors(n)[1:]:
        for sub_ordered_factorization in ordered_factorizations(n/d):
            yield [d]+sub_ordered_factorization


def unordered_factorizations(n, m=None):
    """ Yields unordered factorizations with largest part at most m.
    See: http://www.math.wvu.edu/~mays/Papers/Factorizations.pdf

    If m is not given, yields all unordered factorizations.

    Is not memoized...inefficient"""
    if not m: m = n
    if n == 1: yield []
    if m == 1: yield []
    for d in divisors(n)[1:]:
        if d > m: break
        for sub_unordered_factorization in unordered_factorizations(n/d, d):
            yield [d] + sub_unordered_factorization

def all_factorizations(n, m=None, _memo={}):
    """ Gives a list of all factorizations of n with largest element at most m.
    See:h ttp://www.math.wvu.edu/~mays/Papers/Factorizations.pdf
    
    If m is not given, gives a list of all possible factorizations of n,
    including the trivial factorization [n].

    Do **not** pas argument to _memo, its used for memoization.
    """
    if not m: m=n
    if n == 1: return [[]]
    if m == 1: return [[]]
    if (n,m) not in _memo:
        ans = []
        for d in divisors(n)[1:]:
            if d > m: break
            for sub_factorization in all_factorizations(n/d, d):
                ans.append([d]+sub_factorization)
        _memo[(n,m)] = ans
    return _memo[(n,m)]
        


class TrialDivPrimeTester(object):
    """ A limited primality tester which does trial division with a twist.

    Takes a tuning value during construction, from which it constructs all
    the primes below the value of 10**tuning. Then when testing the primality
    of a number N:
        1. If N <= 10**tuning, does a direct check against the list of primes
        2. If 10**tuning < N < 10**(2*tuning), performs trial division using
           the list of primes.
        3. If N =< 10**(2*tuning), fails with an error.

    Objects of this type are callable, so the intended usage is:
    >>> prime_tester = TrialDivPrimeTester(4)
    >>> prime_tester(997) # Tests against internal small prime list
    True
    >>> prime_tester(10009) # Tests using trial division with small prime list
    True
    >>> prime_tester(99999999) # Largest testable value
    False
    >>> prime_tester(100000001) # Will fail
    ValueError: We cannot test number greater than 100000000"""

    def __init__(self, tuning):
        """ Create a trial division prime tester which creates a list
        of all primes below 10**tuning. """
        self.small_cutoff = 10**tuning
        self.big_cutoff = 10**(2*tuning)
        self._small_primes = set(bounded_soe(self.small_cutoff))
        self._small_prime_factors = sorted(self._small_primes)

    def __call__(self, n):
        if n < self.small_cutoff:
            return n in self._small_primes
        elif n >= self.big_cutoff:
            raise ValueError('We cannot test number greater than %s'
                             % self.big_cutoff)
        else:
            return self._is_prime_by_trial_division_of_small_primes(n)

    def _is_prime_by_trial_division_of_small_primes(self, n):
        sqrt_n = n**0.5
        for p in self._small_prime_factors:
            if p > sqrt_n:
                return True
            elif n % p == 0:
                return False


def solve_pell(D):
    """ Yield successive solutions x, y to the equation:
        x^2 - Dy^2 = 1
    for squarefree integer D.
    
    See:
        http://http://en.wikipedia.org/wiki/Pell%27s_equation
    """
    D = int(D)
    assert int(D**0.5)**2 != D
    x1, y1 = 0, 0
    cf = utils.contfrac.SquareRootCF(D)
    for h, k in cf.convergents():
        if h*h - D*k*k == 1:
            x1, y1 = h, k
            break
    yield x1, y1
    xj, yj = x1, y1
    xk, yk = x1, y1
    while True:
        xk = x1*xj + D*y1*yj
        yk = x1*yj + y1*xj
        yield xk, yk
        xj, yj = xk, yk


def gcd(a, b):
    """ Computes greatest common divisor of positive integers a and b
    using the Euclidean algorithm. """
    while b:
        b, a = a%b, b
    return a


def coprimes(N):
    """ Generates all relatively prime pairs (a, b) with b < a <= N. """
    def _coprime_gen(n, a=1, b=1):
        # the actual generating function. We don't use directly because
        # the first tuple is (1,1) which voilate b < a.
        yield (a, b)
        k = 1
        while a*k + b <= n:
            for coprimes in _coprime_gen(n, a*k+b, a):
                yield coprimes
            k += 1
    # Skip the first item which is always (1,1)
    cg = _coprime_gen(N)
    next(cg)
    for pair in cg:
        yield pair


def primitive_pythagorean_triples(L, give_sum=False):
    M = int((L/2)**0.5)+1
    for m, n in coprimes(M):
        # Skip m,n with (m-n) even
        if (m-n) % 2 == 1:
            triple = tuple(sorted([m*m-n*n, 2*m*n, m*m+n*n]))
            perim = sum(triple)
            if perim <= L:
                if give_sum: yield perim, triple
                else: yield triple
            else: break
            
def pythagorean_triples(L, give_sum=False):
    """ Generates all pythagorean triples with sum (a+b+c) <= L.

    If give_sum == False, yields pythagorean triples (a,b,c) with a < b < c
    andd a+b+c <= L

    If give_sum == True, yields the tuple (perim, (a,b,c)) where the tuple
    (a,b,c) is as described above, and perim is the sum a+b+c.

    Uses Euclid's formula. Euclid's formula takes positive integers m,n,k, with
    m>n, m-n odd and m,n coprime, and returns the pythagorean triples (a,b,c)
    generated by the formulas:
        a = k*(m^2 - n^2)
        b = k*(m*n)
        c = k*(m^2 + n^2)    
    """
    M = int((L/2)**0.5)+1
    for m, n in coprimes(M):
        # Skip m,n with (m-n) even
        if (m-n) % 2 == 0: continue
        for k in itertools.count(1):
            triple = k*(m*m-n*n), 2*k*m*n, k*(m*m+n*n)
            perim = sum(triple)
            if perim <= L:
                if give_sum: yield perim, tuple(sorted(triple))
                else: yield tuple(sorted(triple))
            else: break
