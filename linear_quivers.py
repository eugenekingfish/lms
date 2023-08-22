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

    def projective_resolution_serre(self):
        output = [] # this stores the projective resolution

        for i in range(self.vertices): # we iterate over the vertices
            res = [] 
            resolved = False 
            inj = self.jectives[i][1] # ith injective
            rev_inj = [inj[1], inj[0]] # reversed ith injective

            while not resolved:
                res.append([rev_inj[0]]) 
                proj = self.jectives[rev_inj[0]-1][0] # projective corresponding to ith injective
                ker = linear_module.kernel(rev_inj, proj)

                if ker == [0,0]:
                    resolved = True

                rev_inj = ker

            if len(res) == 1:
                output.append(res[0])
            else:
                output.append(res)
        return output

    def serre_resolution(self):
        pr = self.projective_resolution_serre()
        values = [[i+1] for i in range(self.vertices)]
        counter = 0
        value = values[0]
        while counter < 6:
            print("value ->", value)
            if len(value) == 1:
                value = pr[value[0] - 1].copy()
            else:
                for i in range(len(value)):
                    value[i] = pr[value[i][0] - 1].copy()
            counter += 1

def simplify(lst):
    new_lst = []
    # This removes all interior lists, so [[1], [2]] --> [1,2]
    for i in range(len(lst)):
        if len(lst[i]) == 1:
            new_lst.append(lst[i])
        else:
            sub_lst = []
            for j in range(len(lst[i])):
                sub_lst.append(lst[i][j][0])
            new_lst.append(sub_lst)


    # Adding zeroes to the relevant sub-lists
    longest_lst = len(max(new_lst))

    for i in range(len(new_lst)):
        new_lst[i].extend([0] * (longest_lst - len(new_lst[i])))

    print(new_lst)
    mat = np.matrix(new_lst, dtype=int).T
    print(mat)
    
    

    def serre_functor_resolution2(self):
        pr = self.projective_resolution() 
        print("PROJ RES:", pr)
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
            print("val ->", val)
            try:
                # we try to apply the Serre functor to  <val>  by seeing whether $(val) 
                # is stored within  <serre_dict>
                if type(val) == type([]) and (type(val[0]) == type([])):
                    val = simplify_lst(val)
                    print("simplified ->", val)
                val = serre_dict[str(val)]

            except KeyError:
                print("keyerror ->", val)
                # if $(val) isn't within  <serre_dict>  , then we must calculate it manually
                new_arr = []
                for elem in val:
                    new_arr.append(serre_dict[str(elem)])
                serre_dict[str(val)] = new_arr
                val = new_arr

            counter += 1


def simplify_lst(lst):
    idx = 0
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

def simplify2(L):
    temp = [len(L[i]) + i for i in range(len(L))]
    length = max(temp)
    N = []
    for i in range(length):
        P = []
        for j in range(i+1):
            if len(L) > j and L[j] != [] and L[j][0] != [0]:
                P.append(L[j][0])
                L[j].pop(0)
        N.append(P)
    return N
    

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
