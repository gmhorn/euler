""" Problem 49

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases
by 3330, is unusual in two ways: (i) each of the three terms are prime, and,
(ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes,
exhibiting this property, but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this
sequence?
"""

import itertools
import math
import utils.numtheory


def are_in_arithmetic_sequence(items):
    diff = items[1] - items[0]
    return all((items[i] - items[i-1] == diff) for i in range(1, len(items)))

def order_digits(int_list):
    """ Takes a iterable of ints, and returns an iterable of strings of modified
    ints, where the digits of the ints have been sorted.

    >>> list(order_digits([4231, 9786]))
    ['1234', '6789']
    """
    str_list = map(str, int_list)
    return map(lambda x: ''.join(x), (sorted(s) for s in str_list))

def digit_permutation_tuples(numbers):
    # 1. For each number in 'numbers', turn it into a string and sort the digits
    #       So [1039, 1049, ...] -> ['0139', '0149', ...]
    numbers = list(numbers)
    str_nums = (sorted(str(number)) for number in numbers)
    digit_ordered_list = map(lambda x: ''.join(x), str_nums)
    # 2. Create a dict from the list in step 1. The key is the sorted digits,
    #    the value is a list of indicies in the list in which it appears.
    #    So if 1039 is item 0 in 'numbers' and item 9301 is item 487 in 'numbers'
    #    we end up with:
    #      index_dict = {..., '0139': [0, 487], ...}
    index_dict = {}
    for index, value in enumerate(digit_ordered_list):
        if value not in index_dict:
            index_dict[value] = [index]
        else:
            index_dict[value].append(index)
    # 3. Get a list of all tuples of shared-value indicies
    #    So if 1039 is item 0 on the list in step 1, and item 9301 is item 487
    #    in step 1, we end up with:
    #       indicies = [..., (0, 487), ...]
    indicies = map(tuple, index_dict.values())
    # 5. Map all the indicies in all the tuples in the list generated in step 4
    #    back to their unpermuted integer values by looking up their indicies
    #    in the list generated in step 1,
    #    So if 1039 is item 0 on the list in step 1 and item 9301 is item 487 in
    #    step 1, we have (recalling indicies = [..., (0, 487), ...]:
    #      [..., (0, 487), ...] -> answer = [..., (1039, 9301), ...]
    answer = []
    for tup in indicies:
        tup_vals = tuple(numbers[index] for index in tup)
        answer.append(tup_vals)
    return answer

def ANSWER():
    """ The arithmetic sequence, 1487, 4817, 8147, in which each of the terms
    increases by 3330, is unusual in two ways: (i) each of the three terms are
    prime, and, (ii) each of the 4-digit numbers are permutations of one
    another.

    There are no arithmetic sequences made up of three 1-, 2-, or 3-digit
    primes, exhibiting this property, but there is one other 4-digit increasing
    sequence.

    What 12-digit number do you form by concatenating the three terms in this
    sequence? """
    # 1. Get a list (iterator really) of all 4-digit primes.
    primes = utils.numtheory.bounded_soe(9999, 1000)
    # 2. Group primes which are permutations together
    permutation_groups = digit_permutation_tuples(primes)
    # 3. Create 3 filters on the permutation groups:
    small_groups = filter(lambda x: len(x) < 3, permutation_groups)
    three_groups = filter(lambda x: len(x) == 3, permutation_groups)
    large_groups = filter(lambda x: len(x) > 3, permutation_groups)
    # 4. Save the three_groups, and create 3-permutation groups from each
    #    group in the large groups (a large group with n>3 primes will
    #    have n-Choose-3 three_groups generated.
    three_groups = list(three_groups)
    for large_group in large_groups:
        three_groups.extend(tuple(sorted(triple)) for triple in
                            itertools.combinations(large_group, 3))
    # 5. Save only the three-groups whose elements are in arithmetic sequence
    arithmetic_three_groups = filter(are_in_arithmetic_sequence, three_groups)
    # 6. Print them out
    for group in arithmetic_three_groups:
        return '%s: %s' % (group, ''.join(map(str, group)))

def TIME_ANSWER(repeats=10):
    import timeit
    time = timeit.timeit("ANSWER()", setup="from __main__ import ANSWER",
                         number=repeats)
    return time/repeats

if __name__ == '__main__':
    import utils
    utils.solution_printer(ANSWER)
