import pandas as pd
from time import time

from linear_quivers import *
from relations import *

df = pd.DataFrame()
start_full = time()
for n in range(1,200):
    start = time()
    rels = [[[i,i+2]] for i in range(1,n-2)]

    for rel in rels:
        lq = linear_quiver(n, rel)
        pr = lq.projective_resolution()
        mat = matrix_of_proj_res(pr)
        result = is_fcy_tf(mat, len(mat) + 1)
        new_record = pd.DataFrame([{"n" : n, "Relations" : rel, "FCY Result" : result}])
        df = pd.concat([df, new_record], ignore_index=True)

    end = time()
    print(n, end-start)
end_full = time()
print("Compute time taken:", end_full-start_full)

print(df)
#df.to_csv("l2.csv", mode = "a", header = False, index = False)
df.to_csv("l2_power.csv")



