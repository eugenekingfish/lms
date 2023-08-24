import pandas as pd
from time import time

from linear_quivers import *
from relations import *

n, k = 5,3

rels = [[[2,5]]]


start = time()
for rel in rels:
    lq = linear_quiver(n, rel)
    #pr = lq.projective_resolution()
    #mat = matrix_of_proj_res(pr)
    #print("rel ->", rel, is_fcy(mat, 50), lq.serre_resolution_fast(50, prnt=False))
    print("rel ->", rel, "output ->", lq.serre_resolution_fast(3, prnt=True))
end = time()

lst = [[5,3,2],[4]]
print(remove_lists_and_zeroes([[5],[3,4],[2]]))
print(calculate_sausages(lst))




#print("\nTotal time ->", end - start, "seconds.")
"""
module = [4,3,2]
module2 = [0,0,2,1]
print(module, "-$->", lq.serre_functor(module))
print(module2, "-$->", lq.serre_functor(module2))
"""



