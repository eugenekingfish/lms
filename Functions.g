LoadPackage("qpa");

# This function modifies the source code of the function DynkinQuiver to create 
# right-oriented type A Dynkin quivers with n vertices.

CreateQuiver := function(n)
  local vertices, arrows, i, Q;
  if n <= 0 then
    Error("The quiver must have at least one vertex.\n");
  fi;

  vertices := List([1..n], i -> String(i));
  arrows := [];

  for i in [1..n-1] do
    Add(arrows, [vertices[i], vertices[i+1], Concatenation("a_",String(i))]);
  od;

  Q := Quiver(vertices, arrows);
  SetIsDynkinQuiver(Q, true);

  return Q;
end;

LengthTwoRelations := function(kQ, K)
  local n, arrows, gens, i, j, k, paths, rel, relations;
  n := Length(VerticesOfQuiver(QuiverOfPathAlgebra(kQ)));

  # n must be greater than 3 for there to be at least one pair of length 2 relations
  if n <= 3 then
    return [];
  fi;

  arrows := [];

  # Obtaining the generators of the quiver algebra
  gens := GeneratorsOfAlgebra(kQ); 

  ## Here we create a new list storing only the generators corresponding to arrows
  for i in [n+1..2*n-1] do
    Add(arrows, gens[i]);
  od;
  ##

  relations := [];

  # Generating all length 2 paths
  paths := [];
  for i in [1..n-2] do
    Add(paths, arrows[i] * arrows[i+1]);
  od;

  Print("All length 2 paths:", paths, "\n");

  for i in [1..Length(paths)-K+1] do
    rel := [];
    for k in [0..K-2] do
      Add(rel, paths[i+k]);
    od;
    for j in [0..K-1] do
      Add(relations, Concatenation(rel, [paths[Length(paths)-j]]));
    od;
  od;

  return relations;
end;

NumberOfLengthTwoRelations := function(n, k)
  return 0.5*(n-k)*(n-(k+1));
end;

# Description: This function tests whether the path algebra kQ is fractional Calabi-Yau
# Parameters:  
#              kQ         -- PathAlgebra
#              max_syzygy -- Integer that is greater than 0 used in Omega-periodicity check.

IsFractionalCalabiYau := function(kQ, max_syzygy)
  local triv_ext_alg, M; 
  if max_syzygy <= 0 then
     Error("max_syzygy must be greater than 0.");
  fi;
  # Determining the trivial extension algebra of the path algebra kQ.
  triv_ext_alg := TrivialExtensionOfQuiverAlgebra(kQ);
  # Determing the enveloping algebra of the trivial extension algebra.
  M := AlgebraAsModuleOverEnvelopingAlgebra(triv_ext_alg);

  # Testing the module for Omega-periodicity
  if IsOmegaPeriodic(M, max_syzygy) = false then
        return false;
      else
        return true;
  fi;
end;

CreateQuotientAlgebra := function(kQ, relations)
  local gb, I;
  gb := GBNPGroebnerBasis(relations, kQ);
  I := Ideal(kQ, gb);
  GroebnerBasis(I, gb);
  return kQ / I;
end;

Q := CreateQuiver(5);
kQ := PathAlgebra(Rationals, Q);
