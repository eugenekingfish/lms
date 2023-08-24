from collections import deque
import numpy as np
from collections import deque
import copy

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

    """
        INPUT: 2D list 
    """
    def serre_prt_one(self, L):
        pr = self.projective_resolution()

        # STEP 1: We get the projectives for each element of each sublist of L and append to N
        N = []
        for sublist in L:
            P = [] 
            for elem in sublist:
                P.append(pr[elem - 1])
            N.append(P)

        # STEP 2

        temp = [len(S) + i - 1 for i in range(len(N)) for S in N[i]]
        length = max(temp)

        T = []
        N_cpy = copy.deepcopy(N)

        for i in range(length + 1):
            U = []
            for j in range(i+1):
                if j < len(N):
                    for R in N[j]:
                        if R != []:
                            U.append(R[0])
                            R.pop(0)
                else:
                    break
            T.append(U)
        return T


    def serre_functor(self, module):
        # Repeated calls to self.take_projective_resolution will call self.projective_resolution 
        # every single time. This is probably bad for larger quivers.
        """
        pr = self.take_projective_resolution(module, proj_res)
        saus = calculate_sausages(pr)
        canc_saus = cancellation(saus)
        """
        canc_saus = self.serre_prt_one(module)
        #remove_lists_and_zeroes(canc_saus)
        canc_saus = cancellation(canc_saus)
        canc_saus = remove_empties(canc_saus)
        return canc_saus

    def take_projective_resolution(self, lst, proj_res):
        pr = [[]]
        pr.extend(proj_res) 
        lst_cpy = copy.deepcopy(lst)
        for i in range(len(lst_cpy)):
            lst_cpy[i] = pr[lst_cpy[i]]
        return lst_cpy


    """
        Faster, less-readable version of serre_resolution
    """
    def serre_resolution_fast(self, max_iter, prnt = False):
        states = [[[i+1]] for i in range(self.vertices)] # Initialising the states to be the projectives [1], [2], ..., [n]
        #proj_res = self.projective_resolution()

        for iteration in range(max_iter):
            if prnt:
                print(iteration, "-->", states)

            terminate = True

            for i in range(self.vertices):
                states[i] = self.serre_functor(states[i])
                L = states[i]
                #non_zero = np.count_nonzero(L)
                non_zero = 0
                for l in L:
                    if l != []:
                        non_zero += 1
                
                
                # If L doesn't contain 1 non-zero element, and its last element isn't i + 1, then 
                # we know that we shouldn't terminate applying the Serre functor.
                if not(L[-1] == [i + 1] and non_zero == 1):
                    terminate = False

            # If terminate is still true after exiting the for loop loop, then we must have reached the final
            # stage of the Serre functor process. Hence, we can stop and return the dimension.
            if terminate:
                if prnt:
                    print("FINAL -->", states)
                return (self.vertices - non_zero, iteration + 1)

        return "max_iter reached: " + str(max_iter)

    def serre_resolution(self, max_iter, prnt = False):
        init_states = [[i+1] for i in range(self.vertices)]
        for k in range(max_iter):
            if prnt:
                print(k, "-->", init_states)

            terminate = True
            for i in range(self.vertices):
                init_states[i] = self.serre_functor(init_states[i])
                L = init_states[i]
                non_zero = np.count_nonzero(L)
                if not(L[-1] == i + 1 and non_zero == 1):
                    terminate = False

            if terminate:
                return (k+1, self.vertices - non_zero)

        return "max_iter reached: " + str(max_iter)

def check_zeroes(L):
    if L != [] and np.count_nonzero(L) == 1 and L[-1] != 0:
        return True
    return False

"""
    Assumptions:
        -- L is a list of sub-lists.
        -- The sub-lists do not contain any lists
"""
def cancellation(L):
    # Handling degenerate cases
    l = len(L)
    if l == 0 or l == 1:
        return L

    """
    Is a deep copy required here? If L is the sausages array, is it necessary to keep it?
    Modification might not affect the algorithm at all.
    """
    L_cpy = copy.deepcopy(L) 

    # Non-degenereate case
    for i in range(len(L_cpy) - 1): 
        j = 0
        while j < len(L_cpy[i]):
            if L_cpy[i][j] in L_cpy[i+1]:
                L_cpy[i+1].remove(L_cpy[i][j])
                L_cpy[i].pop(0)
            else:
                j += 1
    return L_cpy

def remove_empties(L):
    idx = len(L) - 1
    non_empty_found = False

    while idx >= 0:
        if L[idx] == []:
            if non_empty_found:
                L[idx] = []
            else:
                L.pop()
        else:
            non_empty_found = True
        idx -= 1
    return L

"""
    Assumptions:
        -- L is a list containing sub-lists.
        -- The sub-lists all have length 1
"""

def remove_lists_and_zeroes(L):
    idx = len(L) - 1
    non_zero_found = False

    while idx >= 0:
        if L[idx] == []:
            if non_zero_found:
                L[idx] = 0
            else:
                L.pop()
        else:
            non_zero_found = True
            L[idx] = L[idx][0]
        idx -= 1
    return L


def remove_lists(L):
    l = len(L)
    for i in range(l):
        if L[i] == []:
            L[i] = 0
        else:
            L[i] = L[i][0]
    return L

def calculate_sausages(L):
    L_copy = copy.deepcopy(L)
    temp = [len(L_copy[i]) + i for i in range(len(L_copy))]
    length = max(temp)
    N = []
    for i in range(length):
        P = []
        for j in range(i+1):
            if len(L_copy) > j and L_copy[j] != [] and L_copy[j][0] != [0]:
                P.append(L_copy[j][0])
                L_copy[j].pop(0)
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
