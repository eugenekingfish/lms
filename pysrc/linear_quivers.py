import numpy as np
import copy
from linear_module import *

class linear_quiver:
    def __init__(self, vertices, relations):
        """
        Initialises the quiver with the number of vertices and its relations; also computes the 
        projective and injective modules.

        Parameters:

            vertices (int): positive integer representing the number of vertices in the quiver.
            relations (): list of ordered pairs (a,b) with (b > a), where  a  is the source and  b  
            is the target of the relation.
        """
        self.vertices = vertices
        self.relations = relations
        self.__calculate_jectives()


    def __calculate_jectives(self):
        """
        This private method calculates the injective and projective modules.
        Sets self.jectives to be a 2D list of the form [ [nth_proj, nth_inj] ] for 1 <= n <= self.vertices.
        """
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

    ###########
    # Getters
    ###########

    def get_jectives(self):
        return self.jectives

    def get_nth_jective(self, n):
        return self.jectives[n-1]

    def get_nth_projective(self, n):
        return self.jectives[n-1][0]

    def get_nth_injective(self, n):
        return self.jectives[n-1][1]

    
    def projective_resolution(self):
        """
        This function computes the projective resolution.
        """
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

    # Converts the projective resolution into a matrix
    def matrix_of_proj_res(self, proj_res):
        n = len(proj_res)
        mat = np.zeros((n,n), dtype=int)
        for i in range(n):
            mult = 1
            for elem in proj_res[i]:
                mat[i][elem - 1] = 1 * mult
                mult *= -1
        return mat.T

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
                P.append(copy.deepcopy(pr[elem - 1]))
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

    """
        Assumptions:
            -- L is a list of sub-lists.
            -- The sub-lists do not contain any lists
    """
    def __cancellation(self, L):
        # Handling degenerate cases
        l = len(L)
        if l == 0 or l == 1:
            return L

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

    def __remove_empties(self, L):
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

    def serre_functor(self, module):
        # Repeated calls to self.take_projective_resolution will call self.projective_resolution 
        # every single time. This is probably bad for larger quivers.
        canc_saus = self.serre_prt_one(module)
        canc_saus = self.__cancellation(canc_saus)
        canc_saus = self.__remove_empties(canc_saus)
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
    def serre_resolution(self, max_iter, verbose = False):
        states = [[[i+1]] for i in range(self.vertices)] # Initialising the states to be the projectives [1], [2], ..., [n]

        for iteration in range(max_iter):
            if verbose:
                print(iteration, "-->", states)

            terminate = True

            for i in range(self.vertices):
                states[i] = self.serre_functor(states[i])

                L = states[i]
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
                if verbose:
                    print("FINAL -->", states)
                return (self.vertices - non_zero, iteration + 1)

        return "max_iter reached: " + str(max_iter)

# Checks whether the quiver represented by the matrix <mat> is fractional Calabi-Yau by 
# checking whether the matrix has finite order (up to power <max_pwr>)
def is_fcy(mat, max_pwr, verbose = False):
    idty = np.eye(len(mat), dtype = int)
    res = mat
    pwr = 1

    while pwr < max_pwr:
        res = res @ mat
        pwr += 1
        if verbose:
            print("Power: ", pwr)
            print(res)
            print()

        if np.array_equal(res, idty) or np.array_equal(res, -1 * idty):
            return (True, pwr)
    
    return (False, max_pwr)
