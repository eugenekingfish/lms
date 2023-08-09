from collections import deque
from time import time

"""
    Description: This function returns a tuple  (P,I)  , where  a  is a list of projectives and  b  is a list of injectives.
    Input:
        -- n:         total number of vertices in the A_n quiver 
        -- relations: list of relations on the A_n quiver. 

    Note:
        Relations must be of the form  (s, t),  where  s  is the source of the relation (when considered as a path in the quiver)
        and  t  is the target of the relation. Since we only consider A_n quivers, we must have that t > s.
"""
def jectives(n, relations):

    arr = deque([]) # We use deque instead of list to perform a left-append in O(1) time, compared to O(n) for list.
    brr = deque([])

    projectives = deque([])
    injectives = deque([])

    # Generating projectives for a quiver with no relations
    for i in range(n):
        arr.appendleft(i+1)
        brr.appendleft(n-i)
        projectives.append(arr.copy())
        injectives.appendleft(brr.copy())

    for r in relations:
        v = r[1]
        while v <= n:
            for _ in range(r[0]): 
                projectives[v-1].pop() 
            v += 1

        v = r[0]
        while v >= 1:
            for _ in range(n - r[1] + 1):
                injectives[v-1].pop()
            v -= 1

    return projectives, injectives

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

    # This function should return a linear module
    # TODO
    def nth_projective(self, n):
        return 0

    # This function should return a linear module too
    # TODO
    def nth_injective(self, n):
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

s = time()
js = jectives(7,[(2,6)])
f = time()
print("Computed jectives in:", f-s, "seconds.")

display_jectives(js)

#print("PROJECTIVES:\n", js[0])
#print("INJECTIVES:\n", js[1])

