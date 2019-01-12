""" Problem 86

A spider, S, sits in one corner of a cuboid room, measuring 6 by 5 by 3, and a
fly, F, sits in the opposite corner. By travelling on the surfaces of the room,
the shortest "straight line" distance from S to F is 10.

However, there are up to three "shortest" path candidates for any given cuboid
and the shortest route doesn't always have integer length.

By considering all cuboid rooms with integer dimensions, up to a maximum size
of M by M by M, there are exactly 2060 cuboids for which the shortest route
has integer length when M=100, and this is the least value of M for which the
number of solutions first exceeds two thousand; the number of solutions is
1975 when M=99.

Find the least value of M such that the number of solutions first exceeds one
million.
"""

import euler.utils.numtheory

# The insight is to consider flattening the cuboid and looking at the path.
#               _____________
#              |             |
#              |_____________|
#              |             |
#              |             |
#              |             |
#              |             |
#     _________|_____________|_________
#    |         |            /| H       |
#    |_________|__________/__|_________|
#              |        /    |
#              |      /      |
#              |    /        | W
#              |  /     L    |
#              |/____________|
#
# So the shortest path length is S = sqrt((W+H)^2 + L^2)
#
# For any (L, W, H) that meets the criteria, we have (L, W+H, S) a pythagorean
# triplet. Call any (L, W+H, S) that meets this criteria a "spider triple".
#
# So for the maximal cuboid MxMxM we have the maximum perimeter
#    P_M = M*(3 + sqrt(5))

import itertools
import collections

def ANSWER(goal, guess_min, guess_max, results=[]):
    def get_val(arr, i):
        if arr[i] < 0:
            arr[i] = count_cuboids(i)
        return arr[i]
    
    if not results:
        results = [-1]*(guess_max+1)

    mid = guess_min + int((guess_max-guess_min)/2)
    print 'cuboid_count({!s}) = {!s}'.format(mid, get_val(results, mid))
    # ensure we calculate our array val!
    if get_val(results, mid) == goal:
        return mid
    elif get_val(results, mid) < goal:
        print 'FOUND LESS'
        if get_val(results, mid+1) >= goal:
            return mid+1
        return ANSWER(goal, mid, guess_max, results)
    else: #results[mid] > goal
        print 'FOUND MORE'
        if get_val(results, mid-1) < goal:
            return mid
        return ANSWER(goal, guess_min, mid, results)

def TESTANS():
    print ANSWER(1000000, 100, 2000)

def count_cuboids(n):
    pythagorean_legs = collections.defaultdict(list)
    # The longest possible perimeter would be for the triangle generated from
    # a = b = n. That is, where a+b is maximal given fixed n and the restriction
    # that a<=b<=n. We get P_max = n(3+sqrt(5)).
    # This perimeter is used in our pythagorean triple search. But our search
    # needs an integral perimeter. So we floor P_max to an integer and add 1
    # to be safe.
    P_max = int(n*(3+(5**0.5)))+1
    for (x, y, z) in euler.utils.numtheory.pythagorean_triples(P_max):
        if x <= n and y < 2*x:
            pythagorean_legs[x].append(y)
        if y <= n and x < 2*y:
            pythagorean_legs[y].append(x)
    count = 0
    for n, vals in pythagorean_legs.iteritems():
        for ab in vals:
            #if ab <= n:
            #    print '{}<={}'.format(ab, n), int((ab+1)/2)
            #    count += int((ab+1)/2)
            #else:
            #    print '{}>{}'.format(ab, n), int((2*n-ab)/2)
            #    count += int((2*n-ab)/2)
            if ab <= n: a, b = 1, ab-1
            else:       a, b = ab-n, n
            while a <= b:
                #print tuple(sorted([a, b, n]))
                count += 1
                a, b = a+1, b-1
    return count
        
def formable_spider_cuboids(n):
    """ Generates cuboids (a, b, n) where 1<=a<=b<=n and the
    cuboid a x b x n has an integral spider path.

    Conceptually, number of pairs (a, b) that create a cuboid a x b x n such
    that:
        1. the spider length is integral
        2. a <= b <= n
    """
    ans = []
    # The longest possible perimeter would be for the triangle generated from
    # a = b = n. That is, where a+b is maximal given fixed n and the restriction
    # that a<=b<=n. We get P_max = n(3+sqrt(5)).
    # This perimeter is used in our pythagorean triple search. But our search
    # needs an integral perimeter. So we floor P_max to an integer and add 1
    # to be safe.
    P_max = int(n*(3+(5**0.5)))+1
    for (x,y,z) in euler.utils.numtheory.pythagorean_triples(P_max):
        # We find the leg whose length is n, and set ab to be the other one
        if   x == n:     n, ab = x, y
        elif y == n:     n, ab = y, x
        else: continue # Or neither leg has length n, so we try the next triple
        # if ab < n, we just take (1, ab-1), (2, ab-2), ... until a>b
        if ab <= n: a, b = 1, ab-1
        # if ab > n, still have ab-n <= n so we take (ab-n, n), (ab-n+1, n-1),
        # ... until a>b
        if ab > n: a, b = ab-n, n
        while a <= b:
            yield tuple(sorted([a, b, n]))
            a, b = a+1, b-1

def total_spider_cuboids(M):
    for n in range(3, M+1):
        for a, b, c in formable_spider_cuboids(n):
            yield a,b,c

def number_spider_cuboids(M):
    """ Number of formable spider cuboids from all boxes no larger than
    M x M x M.

    Can be obtained by summing, from n=1 to M, the number of formable spider
    cuboids of all boxes with at least 1 side with length n and with no sides
    greater than length n. """
    ans = 0
    for n in range(3, M+1):
        ans += len(list(formable_spider_cuboids(n)))
    return ans

def min_M(number_of_cuboids):
    total = 0
    for M in itertools.count(3):
        total += len(list(formable_spider_cuboids(M)))
        if total >= number_of_cuboids: return M

if __name__ == '__main__':
    #import euler.utils
    #euler.utils.solution_printer(min_M, (1000000,))
    print '-'*20
    spids = list(total_spider_cuboids(20))
    print 'Total spider cuboids:', len(spids)
    for sp in spids:
        print sp
    print '-'*20
    print 'ANS'
    print ANS(20)

def PROFILE():
    import cProfile
    cProfile.run('min_M(1000000)')
