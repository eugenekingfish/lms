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
  local triv_ext_alg, sm, ds, check;
  if max_syzygy <= 0 then
     Error("max_syzygy must be greater than 0.");
  fi;
  # Determining the trivial extension algebra of the path algebra kQ.
  triv_ext_alg := TrivialExtensionOfQuiverAlgebra(kQ);

  sm := SimpleModules(triv_ext_alg);
  ds := DirectSumOfQPAModules(sm);

  # Testing the module for Omega-periodicity
  check := IsOmegaPeriodic(ds, max_syzygy);
  if check = false then
        return false;
      else
        return check;
  fi;
end;
