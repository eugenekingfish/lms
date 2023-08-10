from collections import deque
from time import time

#TODO checkout NETWORK 
"""
    Description: This function returns a tuple  (P,I)  , where  a  is a list of projectives and  b  is a list of injectives.
    Input:
        -- n:         total number of vertices in the A_n quiver 
        -- relations: list of relations on the A_n quiver. 

    Note:
        Relations must be of the form  (s, t),  where  s  is the source of the relation (when considered as a path in the quiver)
        and  t  is the target of the relation. Since we only consider A_n quivers, we must have that t > s.
"""
def jectives_old(n, relations):

    arr = deque([]) # We use deque instead of list to perform a left-append in O(1) time, compared to O(n) for list.
    brr = deque([])

    projectives = deque([])
    #injectives = deque([])

    # Generating projectives for a quiver with no relations
    for i in range(n):
        arr.appendleft(i+1)
        #brr.appendleft(n-i)
        projectives.append(arr.copy())
        #injectives.appendleft(brr.copy())

    for r in relations:
        v = r[1]
        while v <= n:
            for _ in range(r[0]): 
                projectives[v-1].pop() 
            v += 1

        """
        v = r[0]
        while v >= 1:
            for _ in range(n - r[1] + 1):
                injectives[v-1].pop()
            v -= 1
        """

    return projectives 


def display_jectives(jectives):
    s = ""
    t = ""
    n = len(jectives[0])
    for i in range(n):
        for j in range(n):
            try:
                s += str(jectives[0][j][i])
                s += "  "
            except IndexError:
                s += "   "
            try:
                t += str(jectives[1][j][n-i-1])
                t += "  "
            except IndexError:
                t += "   "
        s += "\n"
        t += "\n"
    print(s)
    print("- - " * (n-2))
    print(t)

class linear_quiver:
    # vertices  -- positive integer representing the number of vertices in the quiver 
    # relations -- list of ordered pairs (a,b) with (b > a), where  a  is the source and  b  is the target of the relation.
    def __init__(self, vertices, relations):
        self.vertices = vertices
        self.relations = relations
        self.jectives = []

    def calculate_jectives(self):
        n = self.vertices
        # Generating projectives and injectives for an A_n quiver with no relations
        jectives = [[[i+1,1],[i+1,n]] for i in range(n)]

        for r in self.relations:
            
            # Projectives -- P = (p, q)
            # For each relation r = (a,b), we transform the kth projective from (1,k) --> a+1, for every b <= k <= n. 
            a, b = r
            for v in range(b, n+1):
                # jectives[v-1][0][1] is simply the q from P = (p, q)
                jectives[v-1][0][1] = max(a + 1, jectives[v-1][0][1])

            # Injectives:
            # For each relation r = (a,b), we transform the kth injective from (k,n) --> (k, b-1), for every 1 <= k <= n. 
            for v in range(a, 0, -1):
                jectives[v-1][1][1] = max(b - 1, jectives[v-1][1][1])

        self.jectives = jectives

    def get_jectives(self):
        return self.jectives

    # This function should return a linear module
    def get_nth_projective(self, n):
        if self.jectives == []:
            raise(ValueError("calculate_jectives must be called before using this function."))
        else:
            return self.jectives[n-1][0]

    # This function should return a linear module too
    def get_nth_injective(self, n):
        if self.jectives == []:
            raise(ValueError("ERROR: calculate_jectives must be called before using this function."))
        else:
            return self.jectives[n-1][1]


    def display_jectives(self):
        return 0

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


# Outputs a module -- kernel of the projective cover
# There should be an error if the map from the projective is not surjective
def syzygy(quiver, module):
    return 0

# Output -- list of integers representing the vertices of the projective modules in the projective resolution going backwards
def projective_resolution(quiver, module):
    return 0

lq = linear_quiver(7,[(4,6),(2,4),(1,3),(5,7)])
start = time()
lq.calculate_jectives()
end = time()
print("Calculated jectives in:", end - start)
jectives = lq.get_jectives()
for j in jectives:
    print(j[0])


