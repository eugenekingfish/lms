import pandas as pd
from time import time

from linear_quivers import *
from relations import *

def generate_pass_table(max_pwr, max_n):
    data = np.full((max_n, max_n), np.NaN, dtype=float)
    for n in range(3, max_n + 1):

        start = time()
        for l in range(2, n):
            rels = length_k_relations(n,l)
            passes = 1 # initialise for 1 for the empty relation ()

            for rel in rels:
                lq = linear_quiver(n, rel) 
                pr = lq.projective_resolution()
                mat = matrix_of_proj_res(pr)
                result = is_fcy(mat, max_pwr)

                if result[0] == True:
                    passes += 1
            data[n-1][l-1] = passes / len(rels)
            #data[n-1][l-1] = [passes, len(rels)]


        end = time()
        print(n, end-start)

    labels = [i for i in range(1,n+1)]
    df = pd.DataFrame(data, columns=labels, index=labels)
    df.columns.name = "l"
    print("Total Compute time taken:", end-start)

    print(df)
    df.to_csv("csv/TABLE_TEST_BIG.csv")

generate_pass_table(500, 25)
