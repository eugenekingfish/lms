import pandas as pd
from time import time, sleep

from linear_quivers import *
from relations import *

#n = int(input("Vertices in quiver >> "))
#k = int(input("Length of relations >> "))
#max_iter = int(input("Maximum Serre functor applications >> "))

n = 13
k = 5
max_iter = 20


#rels = length_k_relations(n,k)
rels = [[[2,7],[4,9]]]
print(n, "vertices in quiver.")
print("Computed", k, "length", k, "relations.\n")
print("----------------------------------\n")
sleep(0.5)
for rel in rels:

    lq = linear_quiver(n, rel)
    pr = lq.projective_resolution()
    mat = matrix_of_proj_res(pr)
    temp = mat
    mat = np.eye(len(mat), dtype = int)
    for i in range(15):
        mat = mat @ temp
        print(mat)

    #print("rel ->", rel, "           output ->", lq.serre_resolution_fast(max_iter, True))
    #print(is_fcy(mat, 20))










