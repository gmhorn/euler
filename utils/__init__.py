from __future__ import print_function
import functools
import fractions

def solution_printer(ans_func, args=(), kwargs={}):
    import importlib
    from datetime import datetime
    # Print problem statement in module docstring
    mod_name = ans_func.__module__
    ans_mod = importlib.import_module(mod_name)
    ans_doc = ans_mod.__doc__.strip()
    print('-'*80)
    print(ans_doc)
    print('-'*80)
    # Start timer
    start = datetime.now()
    # Get and print answer
    answer = ans_func(*args, **kwargs)
    print('Answer:', answer)
    # Print running time
    end = datetime.now()
    print('Running time:', end-start)


def memoize(obj):
    """ Memoizing decorator that works on functions, methods, or classes, and
    exposes cache publically.

    See: http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize"""
    cache = obj.cache = {}
    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer

def nCr(N, r):
    """ Computes the number of combinations of N things taken r at a time. """
    N, r = int(N), int(r)
    if (r > N) or (N < 0) or (r < 0):
        return 0
    ans = fractions.Fraction(1, 1)
    for i in range(1, r+1):
        ans = ans * fractions.Fraction(N-(r-i), i)
    return int(ans)
