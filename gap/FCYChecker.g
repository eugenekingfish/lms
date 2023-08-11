Read("Functions.g");
Read("FCY.g");

# This function creates a length n quiver of the form 1 -> 2 -> ... -> n-1 -> n
# and creates a PathAlgebra (kQ) from it over the rationals. 
# Then, it generates all length k relations, and tests whether kQ / I is FCY.

CheckAll := function(n, K, write_output) 
  local fn, Q, kQ, rels, i, quot, result;
  if write_output = true then 
    fn := Concatenation("outputs/output_n", String(n), "_k", String(K), ".txt");
    AppendTo(fn, "n = ", n, "; k = ", K, "\n\n");
  fi;

  Q := CreateQuiver(n);
  kQ := PathAlgebra(Rationals, Q);
  rels := LengthKRelations(kQ, K);
  Print("Calculated ", String(Length(rels)), " length ", String(K), " relations.\n");
  Print("Proceeding to check if FCY...\n\n");

  for i in [2..Length(rels)] do

    if write_output then 
      AppendTo(fn, rels[i], " --- ");
    fi;

    Print("Checking: ", rels[i], "\n");
    quot := CreateQuotientAlgebra(kQ, rels[i]);
    result := IsFractionalCalabiYauAlt(quot, 50);
    Print("Completed FCY check. Result --- ", result, "\n");

    if write_output = true then 
      AppendTo(fn, result, "\n");
    fi;

  od;

  Print("\nCheck complete.\n");
  if write_output = true then
    Print("Written output to: ", fn, "\n");
  fi;
end;
