import itertools
import math
import collections

class SquareRootCF(object):
    """ Represents the continued fraction for sqrt(N) with N not a perfect
    square as a continued fraction. """

    _trip = collections.namedtuple('_trip', ['m', 'd', 'a'])
    
    def __init__(self, N):
        
        # TODO: assert N not perfect square
        self._N = N
        self._calculated = False

    def _calculate(self):
        """ Calculates partial quotients of the (periodic) continued fraction
        expansion of sqrt(n) for n not a perfect square.

        Algorithm from:
            http://en.wikipedia.org/wiki/Methods_of_computing_square_roots

        Meant to only be called once from a "public" method.
        
        Have not evaluated whether algorithm can lose precision for n with
        large period. """
        triples = []
        t = SquareRootCF._trip(0, 1, int(math.floor(self._N**0.5)))
        a_0 = t.a
        # Repeat iterations until we get a triple repeating
        while t not in triples:
            # Calculate the next pertial quotient a_i and add
            # the quotient triple to the list
            triples.append(t)
            m = t.d*t.a - t.m
            d = (self._N - m*m)/t.d
            a = int(math.floor((a_0+m)/d))
            t= SquareRootCF._trip(m, d, a)
        # Once we've found a repeat, we find where t is in our
        # ordered list of quotient triples, and take the slice.
        # The slice before is the non-periodic portion, and the
        # slice after is the periodic portion. We save both.
        break_point = triples.index(t)
        non_periodic, periodic = triples[:break_point], triples[break_point:]
        self._periodic = [x.a for x in periodic]
        self._non_periodic = [x.a for x in non_periodic]
        self._calculated = True

    @property
    def period(self):
        if not self._calculated: self._calculate()
        return len(self._periodic)
    
    def quotients(self):
        """ Returns iterator over the partial quotients. """
        if not self._calculated: self._calculate()
        return itertools.chain(self._non_periodic,
                               itertools.cycle(self._periodic))

    def convergents(self):
        """ Returns iterator over the convergents. """
        h_m2, h_m1 = 0, 1 # h_(n-2) and h_(n-1) seeded to values for h_(-2), h_(-1)
        k_m2, k_m1 = 1, 0 # k_(n-2) and k_(n-1) seeded to values for k_(-2), k_(-1)
        quotients = self.quotients()
        # Calculate iterations, starting with 0th
        for a_n in quotients:
            h_n = a_n*h_m1 + h_m2
            k_n = a_n*k_m1 + k_m2
            yield h_n, k_n
            h_m2, h_m1 = h_m1, h_n # swap for next iteration
            k_m2, k_m1 = k_m1, k_n # swap for next iteration
        h_m2, h_m1 = 0, 1

    def __str__(self):
        if not self._calculated: self._calculate()
        a0 = self._non_periodic[0]
        np = ','.join(map(str, self._non_periodic[1:]))
        p = ','.join(map(str, self._periodic))
        return '[%i;%s(%s)]' % (a0, np, p)
