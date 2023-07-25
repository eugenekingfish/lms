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

  # Determing the enveloping algebra of the trivial extension algebra.
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
      if IsomorphicModules(ds ,N1) then
         return i;
      else
         N0 := N1;
      fi;
   od;
   return "Exceeded maximum syzygy.";
end;
