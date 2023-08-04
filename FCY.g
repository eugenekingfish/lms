LoadPackage("qpa");

# Description: This function tests whether the path algebra kQ is fractional Calabi-Yau
# Parameters:  
#              kQ         -- PathAlgebra
#              max_syzygy -- Integer that is greater than 0 used in Omega-periodicity check.

IsFractionalCalabiYau := function(kQ, max_syzygy)
  local triv_ext_alg, M, check;
  if max_syzygy <= 0 then
     Error("max_syzygy must be greater than 0.");
  fi;
  # Determining the trivial extension algebra of the path algebra kQ.
  triv_ext_alg := TrivialExtensionOfQuiverAlgebra(kQ);

  # Determining the enveloping algebra of the trivial extension algebra.
  M := AlgebraAsModuleOverEnvelopingAlgebra(triv_ext_alg);

  # Testing the module for Omega-periodicity
  check := IsOmegaPeriodic(M, max_syzygy);
  if check = false then
        return false;
      else
        return check;
  fi;
end;


IsFractionalCalabiYauAlt := function(kQ, max_syzygy)
  local triv_ext_alg, sm, ds, check, N0, N1, i;
  if max_syzygy <= 0 then
     Error("max_syzygy must be greater than 0.");
  fi;
  # Determining the trivial extension algebra of the path algebra kQ.
  Print("Computing trivial extension...\n");
  triv_ext_alg := TrivialExtensionOfQuiverAlgebra(kQ);

  Print("Computing simple modules...\n");
  sm := SimpleModules(triv_ext_alg);

  Print("Computing direct sum of simple modules...\n");
  ds := DirectSumOfQPAModules(sm);

  N0 := ds;

   for i in [1..max_syzygy] do
      Print("Computing syzygy: ", i, "\n");
      N1 := 1stSyzygy(N0);
      if IsomorphicModules(ds, N1) then
         return i;
      else
         N0 := N1;
      fi;
   od;
   return "Exceeded maximum syzygy.";
end;


IsFractionalCalabiYauV3 := function(kQ, max_syzygy)
  local triv_ext_alg, sm, ds, check, N0, N1, i, j, syzygies, iso_check;

  if max_syzygy <= 0 then
     Error("max_syzygy must be greater than 0.");
  fi;

  # Determining the trivial extension algebra of the path algebra kQ.
  Print("Computing trivial extension...\n");
  triv_ext_alg := TrivialExtensionOfQuiverAlgebra(kQ);

  Print("Computing simple modules...\n");
  sm := SimpleModules(triv_ext_alg);
  syzygies := ShallowCopy(sm);

  for i in [1..max_syzygy] do
  iso_check := true; 
  Print("Current syzygy: ", i, "\n");
    for j in [1..Length(VerticesOfQuiver(QuiverOfPathAlgebra(kQ)))] do
      syzygies[j] := 1stSyzygy(syzygies[j]);
      
      # We require syzygies[j] \cong sm[j] \forall 1 \leq j \leq n.
      # Hence, if we find a single non-isomorphic pair, we don't need to bother checking whether
      # the remaining ones are also isomorphic.
      # This is what the iso_check variable is for -- as soon as a single non-isomorphic pair is found,
      # it prevents the remaining syzygies to be checked for isomorphic; hence saving time.

      if iso_check = true and not(IsomorphicModules(syzygies[j], sm[j])) then
        iso_check := false;
      fi;
    od;

    if iso_check = true then
      return i;
    fi;
  od;
  return "Maximum syzygy exceeded!";
end;
