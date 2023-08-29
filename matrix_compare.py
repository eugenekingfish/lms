import pandas as pd
from time import time, sleep

from linear_quivers import *
from relations import *


n = 7
max_iter = 9

states = [[i+1] for i in range(n)]

def convert_res_to_matrix(res):
    N = 7
    mat = np.zeros((N,N), dtype=int)
    for i in range(len(res)):
        mult = 1
        for j in range(len(res[i])):
            #print(j, res[i][j])
            for k in range(len(res[i][j])):
                if res[i][j] != []:
                    num = res[i][j][k]
                    mat[i][num-1] += mult
            mult *= -1 
    return mat.T


#rels = length_k_relations(n,k)
rel = [[2,5]]

lq = linear_quiver(n, rel)
#print(lq.serre_prt_one([[], [], [5, 7], [3, 4, 4], [2, 1]]))
pr = lq.projective_resolution()
mat = matrix_of_proj_res(pr)
temp = mat
mat = np.eye(len(mat), dtype = int)

mats_a = []
mats_b = []
for i in range(1,10):
    mat = mat @ temp
    mats_a.append(mat)
    #states = lq.serre_functor(states)
    #print("STATES =>\n", states, "\n")
    print("POWER =>", i, "\n")
    print(mat, "\n")
    #print("SERRE MAT =>\n")
    #print(convert_res_to_matrix(states))
    print("-" * 100 + "\n")

STATES = lq.serre_resolution_fast(max_iter, False)

for state in STATES:
    print(state)
    mat = convert_res_to_matrix(state)
    mats_b.append(mat)
    print(mat)
    print("\n")


    #print(is_fcy(mat, 20))

for i in range(len(mats_a)):
    if np.array_equal(mats_a[i], mats_b[i]):
        print("SAME\n", mats_b[i])
    else:
        print("NOT SAME\n", mats_a[i], "\n",mats_b[i])

print("-->\n", convert_res_to_matrix([[[3],[2],[3]], [[],[]]]))
