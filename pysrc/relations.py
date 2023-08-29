from itertools import combinations

def length_k_relations(n, k):
    rels = [(i,i+k) for i in range(1,n-k+1)]
    out = []
    for m in range(1, len(rels) + 1):
        out.extend(combinations(rels, m))
    return out
