import pandas as pd
from time import time

from linear_quivers import *
from relations import *

start = time()
df = pd.DataFrame()
rels = [[1,4],[3,6]]
for n in range(6,500):
    lq = linear_quiver(n, rels)
    pr = lq.projective_resolution()
    mat = matrix_of_proj_res(pr)
    result = is_fcy(mat, 100)
    new_record = pd.DataFrame([{"n" : n, "Relations" : rels, "FCY Result" : result}])
    df = pd.concat([df, new_record], ignore_index=True)

    end = time()
print("Compute time taken:", end-start)

print(df)
df.to_csv("prob_relation_2.csv")



