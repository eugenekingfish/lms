from linear_quivers import *
from relations import *
from time import time, sleep

step_through_mode = False

n = int(input("Enter number of vertices in quiver: "))
k = int(input("Enter length of relations: "))
max_iter = int(input("Enter maximum Serre functor applications: "))

start = time()
rels = length_k_relations(n,k)
end = time()

print(("-" * 100) + "\n")

print("-> Linear quiver contains", n, "vertices.")
print("-> Computed", len(rels), "length", k, "relations in", end - start, "seconds.\n")

print(("-" * 100) + "\n")

start = time()

for rel in rels:
    lq = linear_quiver(n, rel)
    pr = lq.projective_resolution()
    print("Relation ->", rel, "\nOutput ->", lq.serre_resolution_fast(max_iter, False))
    print("\n" + ("-" * 100) + "\n")
    if step_through_mode:
        while True:
            inpt = input("Enter 'y' to proceed to next relation: ")
            if inpt == 'y':
                break
end = time()

print("=> FINISHED COMPUTATION IN", end - start, "SECONDS.\n")
