""" Problem 4

A palindromatic numbe reads the same both ways. The largest palindrome
made from the product of two 2-digit numbers is 9009 = 91 * 99.

Find the largest palindrome made from the product of two 3-digit numbers.
"""

import math

def is_palindrome(n):
    n = str(n)
    return all(n[i] == n[-(i+1)] for i in range(int(0.5*len(n))))

def ANSWER():
    # We'll generate all possible products like so:
    #   999, 999  (-0 from maximum of 999,999)
    #  ----------------------------------------
    #   999, 998  (-1 from maximum of 999,999)
    #  ----------------------------------------
    #   999, 997  (-2 from maximum of 999,999)
    #   998, 998  (-2 from maximum of 999,999)
    #  ----------------------------------------
    #   999, 996  (-3 from maximum)
    #   998, 997  (-3 from maximum)
    #  ----------------------------------------
    #   999, 995  (-4 from maximum)
    #   998, 996  (-4 from maximum)
    #   997, 997  (-4 from maximum)
    # And so on.
    # This generates the list of all unique products, starting
    # with the largest. Similar to the "dovetailing" procedure
    # used to put the rationals in cardinality with the integers.
    # Then we simply test each one for product-palindromeness and
    # return when done.
    for m in range(2, 2000):
        for i in range(1, int(m/2)+1):
            a = 1000 - i
            b = 1000 - (m-i)
            if is_palindrome(a*b):
                # Note: We may be returning prematurely if a later "split" of
                # m produces multiplicands which multiply to a larger number.
                # Really, we should be doing a max() on SOMEthing
                return a, b, a*b

if __name__ == '__main__':
    import utils
    utils.solution_printer(ANSWER)
