import numpy as np

mat = np.matrix(
        [[0, -1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, 0, -1, 0, 0],
        [1, 1, 0, 0, 0, -1, 0],
        [0, 0, 0, 0, 0, 0, -1],
        [0, 0, 1, 1, 1, 1, 1]]
        )

matt = np.matrix(
        [[0, 0, 1, 0, 0, -1, -1],
        [0, 0, -1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, 0, 0, -1, 0],
        [0, 1, 1, 0, 0, 0, -1],
        [0, 0, 0, 1, 1, 1, 1]]
        )

def gen_ident(n):
    out = []
    for i in range(n):
        arr = [0] * n
        arr[i] = 1
        out.append(arr)
    return np.matrix(out)


ident = gen_ident(7)

for i in range(1,10**3):
    mat = mat @ mat
    if (mat == ident).all() or (mat == -1 * ident).all():
        print("Matrix reached +/- the identity in:", i, "steps.")
        break
print("Maximum iterations exceeded!")
print(mat)

