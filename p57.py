""" Problem 57

It is possible to show that the square root of two can be expressed as an
infinite continued fraction.

    sqrt(2) = 1 + 1/(2 + 1/(2 + 1/(2 + ...))) = 1.414213...

By expanding this for the first four iterations we get:
    1 + 1/2 = 3/2 = 1.5
    1 + 1/(2 + 1/2) = 7/5 = 1.4
    1 + 1/(2 + 1/(2 + 1/2)) = 17/12 = 1.41666...
    1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29 = 1.41379...

The next three expansions are 99/70, 239/169, and 577/408, but the eighth
expansion, 1393/985, is the first example where the number of digits in the
numerator exceeds the number of digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator
with more digits than denominator?
"""

import utils.contfrac

def more_digits(h, k):
    """ Returns true if h has more digits than k. """
    return len(str(h)) > len(str(k))

def ANSWER():
    cf = utils.contfrac.SquareRootCF(2)
    convergents = cf.convergents()
    topheavy_convergents = 0
    for i in range(1000):
        h, k = next(convergents)
        if more_digits(h, k): topheavy_convergents+=1
    return topheavy_convergents
        
if __name__ == '__main__':
    import utils
    utils.solution_printer(ANSWER)
