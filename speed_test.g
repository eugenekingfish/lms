Read("Functions.g");
Read("FCY.g");

# This function creates a length n quiver of the form 1 -> 2 -> ... -> n-1 -> n
# and creates a PathAlgebra (kQ) from it over the rationals. 
# Then, it generates all length k relations, and tests whether kQ / I is FCY.

CheckAll := function(n, K, variant)
  local fn, Q, kQ, rels, i, quot, result, t1, t2;
  t1 := Runtime();

  Q := CreateQuiver(n);
  kQ := PathAlgebra(Rationals, Q);
  rels := LengthKRelations(kQ, K);
  Print("Calculated ", String(Length(rels)), " length ", String(K), " relations.\n");
  Print("Proceeding to check if FCY...\n\n");

  for i in [2..Length(rels)] do

    Print("Checking: ", rels[i], "\n");
    quot := CreateQuotientAlgebra(kQ, rels[i]);
    if variant = 1 then
      result := IsFractionalCalabiYau(quot, 4*n);
    fi;

    if variant = 2 then
      result := IsFractionalCalabiYauAlt(quot, 4*n);
    fi;

    if variant = 3 then
      result := IsFractionalCalabiYauV3(quot, 30);
    fi;

    Print("Completed FCY check. Result --- ", result, "\n");

  od;

  Print("\nCheck complete.\n");
  t2 := Runtime();
  Print("Time taken: ", StringTime(t2-t1));
end;
