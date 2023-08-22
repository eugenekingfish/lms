from collections import deque
import numpy as np
from collections import deque

class linear_quiver:
    # vertices  -- positive integer representing the number of vertices in the quiver 
    # relations -- list of ordered pairs (a,b) with (b > a), 
    #              where  a  is the source and  b  is the target of the relation.
    def __init__(self, vertices, relations):
        self.vertices = vertices
        self.relations = relations
        self.calculate_jectives()

    def calculate_jectives(self):
        n = self.vertices
        # Generating projectives and injectives for an A_n quiver with no relations
        jectives = [[[i+1,1],[i+1,n]] for i in range(n)]

        for r in self.relations:
            a, b = r
            for v in range(b, n+1):
                jectives[v-1][0][1] = max(a + 1, jectives[v-1][0][1]) 
            for v in range(a, 0, -1):
                jectives[v-1][1][1] = min(b - 1, jectives[v-1][1][1])

        self.jectives = jectives

    def get_jectives(self):
        return self.jectives

    def get_nth_projective(self, n):
        return self.jectives[n-1][0]

    def get_nth_injective(self, n):
        return self.jectives[n-1][1]

    def projective_resolution(self):
        output = [] # this stores the projective resolution

        for i in range(self.vertices): # we iterate over the vertices
            res = [] 
            resolved = False 
            inj = self.jectives[i][1] # ith injective
            rev_inj = [inj[1], inj[0]] # reversed ith injective

            while not resolved:
                res.append(rev_inj[0]) 
                proj = self.jectives[rev_inj[0]-1][0] # projective corresponding to ith injective
                ker = linear_module.kernel(rev_inj, proj)

                if ker == [0,0]:
                    resolved = True

                rev_inj = ker

            output.append(res)
        return output

    def serre_functor_resolution2(self):
        pr = self.projective_resolution() 
        serre_dict = {} # this stores the (A : B), where A --$--> B

        # initialising  <serre_dict>  with projective resolution  <pr>
        serre_dict['0'] = 0
        for i in range(len(pr)):
            if len(pr[i]) == 1:
                serre_dict[str(i+1)] = pr[i][0]
            else:
                serre_dict[str(i+1)] = pr[i]

        val = 1
        counter = 0

        while counter < 6:
            try:
                # we try to apply the Serre functor to  <val>  by seeing whether $(val) 
                # is stored within  <serre_dict>
                if type(val) == type([]) and (type(val[0]) == type([])):
                    val = simplify_lst(val)
                val = serre_dict[str(val)]

            except KeyError:
                # if $(val) isn't within  <serre_dict>  , then we must calculate it manually
                new_arr = []
                for elem in val:
                    new_arr.append(serre_dict[str(elem)])
                serre_dict[str(val)] = new_arr
                val = new_arr
                print(val)

            counter += 1


def simplify_lst(lst):
    idx = 0
    print("lst", lst)
    while len(lst) != 1:
        current = lst[0][idx]
        if current == lst[1] or current in lst[1]:
            lst[0][idx] = 0
            if type(lst[1]) == type([]):
                lst[1].remove(current)
            else:
                lst.pop(1)
        if len(lst[1]) == 1:
            lst[0].extend(lst[1])
            lst.pop(1)
        idx += 1
    return lst[0]

# We represent the zero module as head = 0, socle = 0.
class linear_module:
    def __init__(self, head, socle):
        if head < socle:
            raise("ERROR: Not valid module. socle > head")
        self.head = head
        self.socle = socle

    # Checks whether the module is the zero module
    def is_zero(self):
        if self.head == 0 and self.socle == 0:
            return True
        return False

    # displays the module vertically
    def display(self):
        return 0
    
    # kernel of two modules
    @staticmethod
    def kernel(mod_a, mod_b):
        a,b = mod_a # we assume that a == b
        c,d = mod_b
        if b == d:
            return [0,0]
        return [max(b,d) - 1, min(b,d)]

# Converts the projective resolution into a matrix
def matrix_of_proj_res(proj_res):
    n = len(proj_res)
    mat = np.zeros((n,n), dtype=int)
    for i in range(n):
        mult = 1
        for elem in proj_res[i]:
            mat[i][elem - 1] = 1 * mult
            mult *= -1
    return mat.T


# Checks whether the quiver represented by the matrix <mat> is fractional Calabi-Yau by 
# checking whether the matrix has finite order (up to power <max_pwr>)
def is_fcy(mat, max_pwr):
    idty = np.eye(len(mat), dtype = int)
    res = mat
    pwr = 1

    while pwr < max_pwr:
        res = res @ mat
        pwr += 1

        if np.array_equal(res, idty) or np.array_equal(res, -1 * idty):
            return (True, pwr)
    
    return (False, max_pwr)
