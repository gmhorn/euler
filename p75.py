""" Problem 75

It turns out that 12 cm is the smallest length of wire that can be bent to form
an integer sided right angle triangle in exactly one way, but there are many
more exaples.

    12 cm: (3,4,5)
    24 cm: (6,8,10)
    30 cm: (5,12,13)
    36 cm: (9,12,15)
    40 cm: (8,15,17)
    48 cm: (12,16,20)

In contrast, some lengths of wire, like 20 cm, cannot be bent to form an integer
sided right angle triangle, and other lengths allow more than one solution to
be found; for example, using 120 cm it is possible to form exactly three
different integer sided right angle triangles.

    120 cm: (30,40,50), (20,48,52), (24,45,51)

Given that L is the length of the wire, for how many valies of L <= 1,500,000
can exactly one integer sided right angle triangle be formed?
"""

import collections
import unittest
import itertools


def gcd(a, b):
    """ Euclidean algorithm. """
    while b:
        b, a = a%b, b
    return a


def coprime_gen(n):
    """ Yields all relatively prime pairs (a, b) with b < a <= n. """
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
    cg = _coprime_gen(n)
    next(cg)
    for pair in cg:
        yield pair


def euclid_formula(k,m,n):
    """ Computes the triple (a,b,c) from (k,m,n) using Euclid's formula.

    For m,n,k natural numbers, with m>n, m-n odd and m, n coprime, returns
    (a,b,c) generated from the formulae:
        a = k*(m^2 - n^2)
        b = k*(m*n)
        c = k*(m^2 + n^2)
    """
    k, m, n = int(k), int(m), int(n)
    assert m>n
    assert (m-n) % 2 == 1
    return (k*(m*m - n*n), 2*k*m*n, k*(m*m + n*n))


def unique_pythagorean_perimeters(L):
    """ Counts the number of perimeters p <= P which have one and only one
    pythagorean triple (a,b,c) whose sum a+b+c equals p. """
    num_triples = collections.defaultdict(int)
    for perim, triple in pythagorean_triple_gen(L):
        num_triples[perim] += 1
    unique_elems = 0
    for count in num_triples.values():
        if count == 1: unique_elems+=1
    return unique_elems
    

def pythagorean_triple_gen(L):
    """ Generates all pythagorean triples with perimeter (a+b+c) <= L.

    Yields tuples (perim, (a,b,c)) where (a,b,c) is a pythagorean triple,
    perim = a+b+c, the triple is in ascending order (a < b < c), and perim <= L
    """
    M = int((L/2)**0.5)+1
    for m, n in coprime_gen(M):
        # Skip m,n with (m-n) even
        if (m-n) % 2 == 0: continue
        for k in itertools.count(1):
            triple = euclid_formula(k,m,n)
            perim = sum(triple)
            if perim <= L:
                yield perim, tuple(sorted(triple))
            else: break

def pythagorean_triples(L):
    """ Gives all pythagorean triples with perimeter (a+b+c) <= L.

    Returns a dict whose keys are the lengths L and whose values are a list of
    triple tuples (a,b,c) whose sum adds to L. """
    d = collections.defaultdict(list)
    for perim, trip in pythagorean_triple_gen(L):
        d[perim].append(trip)
    return d


def brute_pythagorean_triples(L):
    d = collections.defaultdict(list)
    for a in range(1, int(L/2)):
        for b in range(1, a):
            c_f = (a**2 + b**2)**0.5
            c_i = int(c_f)
            if c_f == c_i and (a+b+c_i) <= L:
                d[a+b+c_i].append(tuple(sorted((a,b,c_i))))
    return d


class TestProblem75(unittest.TestCase):

    def assert_dict_matches(self, expect_dict, actual_dict):
        self.assertItemsEqual(expect_dict.keys(), actual_dict.keys())
        for k in sorted(expect_dict.keys()):
            self.assertItemsEqual(sorted(expect_dict[k]),
                                  sorted(actual_dict[k]))

    def test_generates_no_repeats(self):
        d = pythagorean_triples(10000)
        for k, triples in d.iteritems():
            self.assertEqual(len(set(triples)), len(triples))

    def test_unique_permiters_matches_brute_100(self):
        d = brute_pythagorean_triples(100)
        expect = unique_pythagorean_perimeters(100)
        actual = 0
        for k, v in d.items():
            if len(v) == 1:
                actual += 1
        self.assertEqual(expect, actual)
        
    def test_matches_brute_100(self):
        expect = brute_pythagorean_triples(100)
        actual = pythagorean_triples(100)
        self.assert_dict_matches(expect, actual)
    
    def test_correctness_of_brute_triples_100(self):
        error_str = '{!s}^2 + {!s}^2 != {!s}^2'
        d = brute_pythagorean_triples(100)
        for triples in d.values():
            for a,b,c in triples:
                self.assertEqual(a*a + b*b, c*c, error_str.format(a, b,c))

    def test_correctness_of_triples_100(self):
        error_str = '{!s}^2 + {!s}^2 != {!s}^2'
        d = pythagorean_triples(100)
        for triples in d.values():
            for a,b,c in triples:
                self.assertEqual(a*a + b*b, c*c, error_str.format(a, b,c))

    def test_matches_brute_1000(self):
        expect = brute_pythagorean_triples(1000)
        actual = pythagorean_triples(1000)
        self.assert_dict_matches(expect, actual)

def TIMEIT():
    import timeit
    print('Brute force method. L = 1000')
    print(timeit.timeit('brute_pythagorean_triples(1000)',
                        setup='from __main__ import brute_pythagorean_triples',
                        number=1))

    print('-'*39)
    print('Euclid method. L = 1000')
    ''
    print(timeit.timeit('pythagorean_triples(1000)',
                        setup='from __main__ import pythagorean_triples',
                        number=1))
    
    print('-'*39)
    print('Euclid method. L = 100000')
    print(timeit.timeit('pythagorean_triples(100000)',
                        setup='from __main__ import pythagorean_triples',
                        number=1))

    print('-'*39)
    print('Count unique perimeters. L = 100000')
    print(timeit.timeit('unique_pythagorean_perimeters(100000)', number=1,
          setup='from __main__ import unique_pythagorean_perimeters'))

    print('-'*39)
    print('Count unique perimeters. L = 1000000')
    print(timeit.timeit('unique_pythagorean_perimeters(1000000)', number=1,
          setup='from __main__ import unique_pythagorean_perimeters'))

def PROFILE():
    import cProfile
    cProfile.run('unique_pythagorean_perimeters(100000)')

def TEST():
    unittest.main(verbosity=2, exit=False)


if __name__ == '__main__':
    import utils
    utils.solution_printer(unique_pythagorean_perimeters, (1500000,))

