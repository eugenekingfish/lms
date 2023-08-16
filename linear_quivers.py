from collections import deque
import tensorflow as tf
import numpy as np

class linear_quiver:
    # vertices  -- positive integer representing the number of vertices in the quiver 
    # relations -- list of ordered pairs (a,b) with (b > a), where  a  is the source and  b  is the target of the relation.
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

    # This function should return a linear module
    def get_nth_projective(self, n):
        return self.jectives[n-1][0]

    # This function should return a linear module too
    def get_nth_injective(self, n):
        return self.jectives[n-1][1]


    # This function partially works
    def display_jectives(self, pad = 2):
        s = ""
        print(self.jectives)
        for i in range(self.vertices):
            counter = 1
            for j in range(self.vertices):
                if j < i:
                    s += " " +  (" " * pad)
                if j >= i:
                    if self.jectives[j][0][1] <= counter:
                        s += str(counter) + (" " * pad)
                    counter += 1
            s += "\n"
        print(s)

    def projective_resolution(self):
        output = []
        for i in range(self.vertices):
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
        a,b = mod_a
        c,d = mod_b
        if b == d:
            return [0,0]
        return [max(b,d) - 1, min(b,d)]

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

# Performs the same operation as is_fcy, but utilises Tensorflow for GPU matmul optimisation
def is_fcy_tf(mat, max_pwr):
    idty = np.eye(len(mat), dtype = int)
    res = mat
    pwr = 1

    while pwr < max_pwr:
        tensor_res = tf.convert_to_tensor(res)
        tensor_mat = tf.convert_to_tensor(mat)
        res = tf.matmul(res, mat)
        pwr += 1

        if np.array_equal(res.numpy(), idty) or np.array_equal(res.numpy(), -1 * idty):
            return (True, pwr)
    
    return (False, max_pwr)

def is_fcy_l2_tf(mat, pwr):
    idty = np.eye(len(mat), dtype = int)
    tensor_mat = tf.convert_to_tensor(mat)
    power = tf.linalg.matrix_power(tensor_mat, pwr)

    if np.array_equal(power.numpy(), idty) or np.array_equal(power.numpy(), -1 * idty):
        return (True, pwr)
    
    return (False, pwr)
