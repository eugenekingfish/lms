import pandas as pd
from time import time

from linear_quivers import *
from relations import *

df = pd.DataFrame()
for n in range(25):
    start = time()
    rels = length_k_relations(n,9)

    for rel in rels:
        lq = linear_quiver(n, rel)
        pr = lq.projective_resolution()
        mat = matrix_of_proj_res(pr)
        result = is_fcy(mat, 250)
        new_record = pd.DataFrame([{"n" : n, "Relations" : rel, "FCY Result" : result}])
        df = pd.concat([df, new_record], ignore_index=True)

    end = time()
    print(n, end-start)
print("Compute time taken:", end-start)

print(df)
df.to_csv("l9_relations.csv")



