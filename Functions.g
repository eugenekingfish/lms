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

MaximalPaths := function(Q)
  local paths, verts, i, j, k, l, targets, out_arrow, out_arrows;

  verts := VerticesOfQuiver(Q);
  paths := [];

  for i in [1..Length(verts)] do
    targets := [];
    Append(paths, [[]]);
    out_arrows := OutgoingArrowsOfVertex(verts[i]);
    Append(paths[i], out_arrows); # Adding the outgoing arrows to the paths

    while not(out_arrows = []) do
       # Obtaining a list of targets for the outgoing arrows
       for j in [1..Length(out_arrows)] do
          Append(targets, [TargetOfPath(out_arrows[j])]);
       od;
       out_arrows := [];
       for k in [1..Length(targets)] do
          Append(out_arrows, [OutgoingArrowsOfVertex(targets[k])]);
       od;
       Print(targets, "\n");
    od;
  od;
  return paths;
end;

Q := CreateQuiver(5);
m := MaximalPaths(Q);
Print(m, "\n");
