""" Problem 122

The most naive way of computing n^15 requires fourteen multiplications:
    n*n*...*n = n^15

But using a "binary" method you can compute it in six multiplications:
    n * n = n^2
    n^2 * n^2 = n^4
    n^4 * n^4 = n^8
    n^8 * n^4 = n^12
    n^12 * n^2 = n^14
    n^14 * n = n^15

However it is yet possible to compute it in only five multiplications:
    n * n = n^2
    n^2 * n = n^3
    n^3 * n^3 = n^6
    n^6 * n^6 = n^12
    n^12 * n^3 = n^15

We shall define m(k) to be the minimum number of multiplications to
compute n^k; for example, m(15) = 5.

For 1 <= k <= 200, find sum(m(k)).
"""

def all_m(kmax, _path=[1], _mvals={}):
    """ returns a dict of all {k: m(k) for k in [1, kmax]}.

    Performs a DFS. At any stage we have a path [1, 2,..., v] representing an
    addition chain (each a_m = a_(m-1) + a_i where is is 1,2,...,m-1). """
    if _path:
        k = _path[-1]
        m = len(_path)-1
        if k <= kmax and (k not in _mvals or m <= _mvals[k]):
            _mvals[k] = m
            for e in reversed(_path):
                new_k = k + e
                find_all_m(kmax, _path + [new_k], _mvals)
    return _mvals

def ANSWER():
    return sum(all_m(200).itervalues())

if __name__ == '__main__':
    import euler.utils
    euler.utils.solution_printer(ANSWER)
