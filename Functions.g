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





# TODO: error checking -- test whether kQ is a pathalgebra and if the underlying quiver is dynkin a
LengthTwoRelations := function(kQ)
  local n, arrows, gens, i, j, r1, r2, length_two_relations;
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

  length_two_relations := [];

  for i in [1..n-2] do
    r1 := arrows[i] * arrows[i+1];
    for j in [i+1..n-2] do
      r2 := arrows[j] * arrows[j+1];
      Add(length_two_relations, [r1, r2]);
    od;
  od;
  return length_two_relations;
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
