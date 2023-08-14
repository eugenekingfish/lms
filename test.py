from linear_quivers import *
from time import time

lq = linear_quiver(5,[(2,4)])
lq.calculate_jectives()
pr = lq.projective_resolution()
mat = matrix_of_proj_res(pr)
print("Matrix of projective resolution:\n\n", mat)
print(is_fcy(mat, 12))
