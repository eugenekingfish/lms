from itertools import combinations

def length_two_relations(n):
    rels = [[i,i+2] for i in range(1,n-1)]
    out = []
    for m in range(1, len(rels) + 1):
        out.extend(combinations(rels, m))
    return out

def length_k_relations(n, k):
    rels = [[i,i+k] for i in range(1,n-k+1)]
    out = []
    for m in range(1, len(rels) + 1):
        out.extend(combinations(rels, m))
    return out

