import itertools
import numbers
import bisect

class PolyError(Exception):
    pass


def _trim_array(iterable, tol=0):
    """ Turns iterable into a list with trailing values of (absolute)
    magnitude less than or equal to `tol` removed.

    If the result is an empty list, returns instead the "null list" [0]

    >>> _trim_array([0, 1, 2, 3])
    [0, 1, 2, 3]
    >>> _trim_array([0, 1, 0, 2, 0, 0])
    [0, 1, 0, 2]
    >>> _trim_array([0, 1, 0, 2, -0.001, 0.001], tol=0.01)
    [0, 1, 0, 2]
    """
    a = list(iterable)
    while len(a) and abs(a[-1]) <= tol:
        a = a[:-1]
    if not a: a = [0]
    return a


def _print_terms(poly):
    # Immediately return for null polynomial
    if not poly: return '0'
        
    first = True # marks first term
    retstr = ''
    for e, a in enumerate(poly.coeffs):
        if not a: continue
        # Find x term
        if   e == 0: x_term = ''
        elif e == 1: x_term = 'x'
        else       : x_term = 'x^{!s}'.format(e)
        # Find a term
        if abs(a) == 1 and e != 0:
            a_term = ''
        else: a_term = str(abs(a))
        # Find sign (affected by first term!)
        if not first:
            if a < 0: a_sign = ' - '
            else    : a_sign = ' + '
        else:
            if a < 0: a_sign = '-'
            else    : a_sign = ''
            first = False
        retstr = retstr + a_sign + a_term + x_term
    return retstr


class Poly(object):

    def __init__(self, coeff):
        if isinstance(coeff, numbers.Number):
            coeff = [coeff]
        self._coeff = _trim_array(coeff)

    def __str__(self):
        return 'p(x) = '+_print_terms(self)

    def __repr__(self):
        return 'Poly({!r})'.format(self._coeff)

    def __call__(self, x):
        """ Evaluates the polynomial for a given value of x. """
        return sum(a*(x**e) for e, a in enumerate(self._coeff))

    @property
    def coeffs(self):
        """ Returns a copy of the coefficients of the polynomial. """
        return list(self._coeff)

    @property
    def degree(self):
        """ Returns the degree of a Polynomial. """
        return len(self._coeff) - 1
    
    def __bool__(self):
        """ Returns False if it is the null polynomial p(x) = 0 """
        return self._coeff != [0]

    __nonzero__ = __bool__
    
    def __add__(self, other):
        if not isinstance(other, Poly):
            other = Poly(other)
        zip_tuples = itertools.izip_longest(self._coeff, other._coeff,
                                            fillvalue=0)
        new_coeffs = list(map(sum, zip_tuples))
        return Poly(new_coeffs)

    def __sub__(self, other):
        if not isinstance(other, Poly):
            other = Poly(other)
        zip_tuples = itertools.izip_longest(self._coeff, other._coeff,
                                            fillvalue=0)
        new_coeffs = list(map(lambda x: x[0]-x[1], zip_tuples))
        return Poly(new_coeffs)

    def __mul__(self, other):
        """ Computes the multiplication of 2 polynomials
        using Cauchy product. """
        if not isinstance(other, Poly):
            other = Poly(other)
        a, b = self.coeffs, other.coeffs
        da, db = self.degree, other.degree
        c = []
        for k in range(0, da+db+1):
            imin = max(0, k-db)
            imax = min(k, da)+1
            ck = sum(a[i]*b[k-i] for i in range(imin, imax))
            c.append(ck)
        return Poly(c)

    def __radd__(self, other):
        if not isinstance(other, numbers.Number):
            return NotImplemented
        other = Poly(other)
        return other + self

    def __rsub__(self, other):
        if not isinstance(other, numbers.Number):
            return NotImplemented
        other = Poly(other)
        return other - self

    def __rmul__(self, other):
        if not isinstance(other, numbers.Number):
            return NotImplemented
        other = Poly(other)
        return other*self

    def __neg__(self):
        return -1*self

NullPoly = Poly(0)
UnitPoly = Poly(1)
