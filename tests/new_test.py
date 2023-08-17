import pandas as pd
from time import time

from linear_quivers import *
from relations import *


lq = linear_quiver(11, [[1,10]])
pr = lq.projective_resolution()
mat = matrix_of_proj_res(pr)
print(mat)




