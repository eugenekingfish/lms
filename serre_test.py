import pandas as pd
from time import time

from linear_quivers import *
from relations import *

n, k = 13,2
rels = length_k_relations(n, k)

start = time()
for rel in rels:
    lq = linear_quiver(n, rel)
    #pr = lq.projective_resolution()
    #mat = matrix_of_proj_res(pr)
    #print("rel ->", rel, is_fcy(mat, 50), lq.serre_resolution_fast(50, prnt=False))
    print("rel ->", rel, "output ->", lq.serre_resolution_fast(40, prnt=False))
end = time()




print("\nTotal time ->", end - start, "seconds.")
"""
module = [4,3,2]
module2 = [0,0,2,1]
print(module, "-$->", lq.serre_functor(module))
print(module2, "-$->", lq.serre_functor(module2))
"""



