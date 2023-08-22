import pandas as pd
from time import time

from linear_quivers import *
from relations import *

lst = [[[4], [3], [2]], [[4]], [[3], [1]]]

lq = linear_quiver(4, [[2,4]])
#lq.serre_resolution()
print(simplify2(lst))
print(lst)





