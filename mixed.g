Read("FCY.g");
Read("Functions.g");

# Given two lists of relations  rel_a  and  rel_b, this function returns a new list containing 
# all unique combinations of relations from each list.

CombineRelations := function(rels_a, rels_b)
  local new_rel, new_rels, i, j;
  new_rels := [];
  for i in [1..Length(rels_a)] do
    for j in [1..Length(rels_b)] do 
      if not(rels_a[i] = []) and not(rels_b[j] = []) then
        new_rel := Concatenation(rels_a[i], rels_b[j]);
        Append(new_rels, [new_rel]);
      fi;
    od;
  od;
  return new_rels;
end;


MixedChecker := function(n, a, b)
  local Q, kQ, rels_a, rels_b, new_rels, i, I, j, k, quot, result;
  Q := CreateQuiver(n);
  kQ := PathAlgebra(Rationals, Q);

  new_rels := CombineRelations(rels_a, rels_b);

  for k in [1..Length(new_rels)] do
    Print("Checking: ", new_rels[k], "\n");
    quot := CreateQuotientAlgebra(kQ, new_rels[k]);
    result := IsFractionalCalabiYauV3(quot, 30);
    Print("Completed FCY check. Result --- ", result, "\n");
  od;

  return new_rels;
end;
