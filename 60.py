import itertools
""" Problem 60

The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes
and concatenating them in any order the result will always be prime. For
example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four
primes, 792, represents the lowest sum for a set of four primes with this
property.

Find the lowest sum for a set of five primes for which any two primes
concatenate to produce another prime.
"""

import euler.utils
import euler.utils.numtheory
import math
import collections

def concat_int(a, b):
    return a*(10**(int(math.log10(b))+1)) + b


def _k_cliques(k, nodes=None, clique=(), ):
    if len(clique) == k:
        print 'Clique found:', clique
        yield clique
    node_set  = set(nodes)
    node_list = list(sorted(nodes))
    for candidate in node_list:
        intersect_nodes = set(pair_partners(candidate)) & node_set
        if len(intersect_nodes) >= k - (len(clique)+1):
            next_cliques = _k_cliques(k, intersect_nodes,
                                     clique + tuple([candidate]))
            for next_clique in next_cliques:
                yield next_clique

class RemarkableCliques(object):

    def __init__(self, limit):
        self._edges = {}
        self._primes = list(euler.utils.numtheory.bounded_soe(limit))
        limit_exp = math.log10(limit) + 1
        self._is_prime = euler.utils.numtheory.TrialDivPrimeTester(limit_exp)

    def _partners(self, p):
        def are_remarkable(a, b):
            return (self._is_prime(concat_int(a, b)) and
                    self._is_prime(concat_int(b, a)))
        if p not in self._edges:
            index = self._primes.index(p)
            self._edges[p] = [q for q in self._primes[index:] if
                              are_remarkable(p, q)]
        return self._edges[p]

    def k_cliques(self, k, nodes=None, clique=()):
        if not nodes and not clique:
            for clique in self.k_cliques(k, self._primes): yield clique
        if len(clique) == k:
            yield clique
        node_set  = set(nodes)
        node_list = list(sorted(nodes))
        for candidate in node_list:
            intersect_nodes = set(self._partners(candidate)) & node_set
            if len(intersect_nodes) + len(clique) + 1 >= k:
                extended_clique = clique + tuple([candidate])
                for new_clique in self.k_cliques(k, intersect_nodes, extended_clique):
                    yield new_clique
                         
class RemarkableFamilyGenerator(object):

    def __init__(self, upper_bound_exp):
        self.pairwise_dict = {}
        upper_bound = 10**upper_bound_exp
        self.primes = list(euler.utils.numtheory.bounded_soe(upper_bound))
        self.is_prime = euler.utils.numtheory.TrialDivPrimeTester(upper_bound_exp)

    def _is_pairwise_remarkable(self, p, q):
        return (self.is_prime(concat_int(p, q)) and
                self.is_prime(concat_int(q, p)))

    def pair_partners(self, p):
        if p not in self.pairwise_dict:
            index = self.primes.index(p)
            self.pairwise_dict[p] = [q for q in self.primes[index:] if
                                     self._is_pairwise_remarkable(p, q)]
        return self.pairwise_dict[p]
            
    def find_k_families(self, k, nodes=None, clique=()):
        if not nodes and not clique:
            return self.find_k_families(k, self.primes)
        if len(clique) == k:
            print 'CLIQUE FOUND:', clique
            return [clique]
        cliques = []
        node_set = set(nodes)
        ordered_nodes = sorted(list(nodes))
        for next_elem in ordered_nodes:
            next_round_nodes = (set(self.pair_partners(next_elem)) &
                                     node_set)
            #print 'clique:', clique
            #print 'next elem:', next_elem
            #if len(next_round_nodes) > 10: ellipses='...'
            #else: ellipses = ''
            #print 'next round nodes:', list(next_round_nodes)[:10], ellipses
            #print 'len(next_round_nodes): %i, k: %i, len(clique): %i' % (len(next_round_nodes), k, len(clique))
            if len(next_round_nodes) >= k-(len(clique)+1):
                new_cliques = self.find_k_families(k, next_round_nodes,
                                                clique + tuple([next_elem]))
                for new_clique in new_cliques:
                    cliques.append(new_clique)
        return cliques
        
def TEST():
    import itertools
    rk = RemarkableCliques(10000)
    g = rk.k_cliques(4)
    print next(g)
    print next(g)
    
    
    
    
def FOUR_ANS(guess):
    primes = list(euler.utils.numtheory.bounded_soe(guess))
    remarkable_partners = RemarkablePartnerGenerator(primes)
    # 1
    for a1 in primes:
        L1 = remarkable_partners(a1)
        if len(L1) < 4: continue
        A1 = frozenset(L1)
        # 2
        for a2 in L1:
            #A2 = set(pairwise_remarkable_with(a2, primes)) & A1
            A2 = frozenset(remarkable_partners(a2)) & A1
            if len(A2) < 3: continue
            L2 = sorted(A2)
            # 3
            for a3 in L2:
                #A3 = set(pairwise_remarkable_with(a3, primes)) & A2
                A3 = frozenset(remarkable_partners(a3)) & A2
                if len(A3) < 1: continue
                L3 = sorted(A3)
                arr = (a1, a2, a3, L3[0])
                return sum(arr), arr
    return -1, ()

def PROFILE():
    import cProfile
    cProfile.run('ANSWER(10000)')

def ANSWER(guess):
    primes = list(euler.utils.numtheory.bounded_soe(guess))
    primes.remove(2); primes.remove(5)
    remarkable_partners = RemarkablePartnerGenerator(primes)
    # 1
    for a1 in primes:
        #L1 = pairwise_remarkable_with(a1, primes)
        L1 = remarkable_partners(a1)
        if len(L1) < 4: continue
        A1 = frozenset(L1)
        # 2
        for a2 in L1:
            # A2 = set(pairwise_remarkable_with(a2, primes)) & A1
            A2 = frozenset(remarkable_partners(a2)) & A1
            if len(A2) < 3: continue
            L2 = sorted(A2)
            # 3
            for a3 in L2:
                # A3 = set(pairwise_remarkable_with(a3, primes)) & A2
                A3 = frozenset(remarkable_partners(a3)) & A2
                if len(A3) < 2: continue
                L3 = sorted(A3)
                # 4
                for a4 in L3:
                    # A4 = set(pairwise_remarkable_with(a4, primes)) & A3
                    A4 = frozenset(remarkable_partners(a4)) & A3
                    if len(A4) < 1: continue
                    L4 = sorted(A4)
                    return sum([a1, a2, a3, a4, L4[0]])
    return -1
"""
if __name__ == '__main__':
    from datetime import datetime, timedelta
    start = datetime.now()
    #print FOUR_ANS(1000)
    print 'Answer: ', ANSWER(10000)
    end = datetime.now()
    print 'Elapsed Time: ', (end-start)
"""
