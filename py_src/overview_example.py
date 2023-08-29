from linear_quivers import *
from relations import *


"""
    A simple example.
"""

# Firstly, we will initialise the variable  n  to store the number of vertices in the linear quiver that 
# we are going to create.

n = 5 

# Next, we will create a list storing the quiver's relations. 
# To start, we'll leave the list empty to represent no relations.

relations = []

# We can now create a linear quiver containing 5 vertices with no relations.

lq = linear_quiver(n, relations)
print("Created a linear quiver quiver containing", n, "vertices with relations:", relations)

# This quiver is of the form: 1 --> 2 --> 3 --> 4 --> 5.

# We can now perform some operations on the quiver.
# For example, we can compute its projective resolution:

proj_res = lq.projective_resolution()
print("Projective Resolution:", proj_res)

# If we want, we can also obtain the kth (in/pro)jective module.
# For example, we can obtain the third injective and projective:

third_injective = lq.get_nth_injective(3)
third_projective = lq.get_nth_projective(3)

print("3rd injective:", third_injective)
print("3rd projective:", third_projective)

# Alternatively, we can obtain both of these at once:
third_jective = lq.get_nth_jective(3)
print("3rd injective:", third_jective[1], " --- ", "3rd projective:", third_jective[0])

# On line 28, we calculated the projective resolution.
# We can convert this to a matrix as follows:

proj_res_mat = lq.matrix_of_proj_res(proj_res)
print("Matrix of projective resolution:")
print(proj_res_mat)

# We can then use this matrix to test whether the linear quiver that we've created is fractional Calabi-Yau.
# This is done by checking whether  proj_res_mat  has finite order.

fcy_check = is_fcy(proj_res_mat, 100)
print("FCY Check ->", fcy_check)

# The second parameter to  is_fcy  is the maximum power to which we will raise the matrix.
# If we set the optional parameter  verbose  to be True, then we can see each matrix power printed.

fcy_check_verbose = is_fcy(proj_res_mat, 100, verbose = True)
print("FCY Check ->", fcy_check_verbose)

# Finally, to find the Calabi-Yau dimension of the quiver, we can do the following:

dimension = lq.serre_resolution(100)
print("Dimension:", dimension)

# Here, the single parameter to  serre_resolution  is the maximum number of times to apply the Serre functor.

# Just like before, we can obtain verbose output:
dimension_verbose = lq.serre_resolution(100, verbose = True)
print("Dimension Verbose:", dimension_verbose)

# END OF FILE
