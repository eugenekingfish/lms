LoadPackage("qpa");

# This function modifies the source code of the function DynkinQuiver to create 
# right-oriented type A Dynkin quivers with n vertices.

CreateQuiver := function(n)
  local vertices, arrows, i, Q;
  if n <= 0 then
    Error("The quiver must have at least one vertex.\n");
  fi;

  vertices := List([1..n], i -> Concatenation("v", String(i)));
  arrows := [];

  for i in [1..n-1] do
    Add(arrows, [vertices[i], vertices[i+1], Concatenation("a",String(i))]);
  od;

  Q := Quiver(vertices, arrows);
  SetIsDynkinQuiver(Q, true);

  return Q;
end;

CreatePathAlgebra := function(n)
  return PathAlgebra(Rationals, CreateQuiver(n));
end;

LengthTwoRelations := function(kQ)
  local n, arrows, gens, relations, i, j, l;
  n := Length(VerticesOfQuiver(QuiverOfPathAlgebra(kQ)));

  arrows := [];

  # Obtaining the generators of the quiver algebra
  gens := GeneratorsOfAlgebra(kQ); 

  ## Here we create a new list storing only the generators corresponding to arrows
  for i in [n+1..2*n-1] do
    Add(arrows, gens[i]);
  od;
  ##

  relations := [ [] ];

  for i in [1..n-2] do 
    j := 1;
    l := Length(relations);
    for j in [1..l] do
      Add(relations, Concatenation(relations[j], [arrows[i] * arrows[i+1]]));
      j := j + 1;
    od;
  od;
  return relations;
end;

LengthKRelations := function(kQ, K)
  local n, arrows, gens, relations, i, j, k, l, current;

  n := Length(VerticesOfQuiver(QuiverOfPathAlgebra(kQ)));
  arrows := [];

  # Obtaining the generators of the quiver algebra
  gens := GeneratorsOfAlgebra(kQ); 

  ## Here we create a new list storing only the generators corresponding to arrows
  for i in [n+1..2*n-1] do
    Add(arrows, gens[i]);
  od;
  ##

  relations := [ [] ];

  for i in [1..n-K] do 
    j := 1;
    l := Length(relations);

    current := arrows[i];
    for k in [1..K-1] do
      current := current * arrows[i+k];
    od;

    for j in [1..l] do
      Add(relations, Concatenation(relations[j], [current]));
      j := j + 1;
    od;
  od;
  return relations;
end;

AllRelations := function(kQ)
  local n_arrows, result, i, temp;

  n_arrows := Length(VerticesOfQuiver(QuiverOfPathAlgebra(kQ))) - 1;
  result := [];

  for i in [1..n_arrows] do
    temp := Concatenation(result, LengthKRelations(kQ, i));
    Append(result, temp);
  od;
  return result;
end;

CreateQuotientAlgebra := function(kQ, relations)
  local gb, I;
  gb := GBNPGroebnerBasis(relations, kQ);
  I := Ideal(kQ, gb);
  GroebnerBasis(I, gb);
  return kQ / I;
end;

TrivA := function(n) 
  local Q, kQ, t1, t2, triv_ext;
  t1 := Runtime();
  Q := CreateQuiver(n);
  kQ := PathAlgebra(Rationals, Q);
  triv_ext := TrivialExtensionOfQuiverAlgebra(kQ);
  t2 := Runtime();
  Print("Time taken: ", StringTime(t2-t1), "\n");
  return triv_ext;
end;

MaximalPaths := function(kQ)
  local Q, i, l, j, out, rels, pa_rels, _kQ;

  Q := QuiverOfPathAlgebra(kQ);
  l := Length(VerticesOfQuiver(Q));
  _kQ := PathAlgebra(Rationals, CreateQuiver(l)); # Duplicate of kQ without relations
  out := [];
  pa_rels := RelationsOfAlgebra(kQ); # Getting relations used in ideal for kQ

  for i in [1..l-2] do
    rels := LengthKRelations(_kQ, l-i);
    for j in [1..Length(rels)] do
      Print(rels[j], " : ", String(rels[j]), " : ", pa_rels, " : ", "\n");
       if not(IsZero(rels[j])) then
         Append(out, rels[j]);
       fi;
    od;

    if not(out = []) then
      return out;
    fi;
  od;
end;
