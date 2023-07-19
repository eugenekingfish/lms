LoadPackage("qpa");

q := Quiver(3, [[1, 2, "a"], [2, 3, "b"]]);
qq := Quiver(4, [[1, 2, "a"], [2, 3, "b"], [3, 4, "c"]]);
qq_pa := PathAlgebra(Rationals, qq);
q_pa := PathAlgebra(Rationals, q);

kron := KroneckerAlgebra(Rationals, 2);

# Description: This function tests whether the path algebra kQ is fractional Calabi-Yau
# Parameters:  
#              kQ         -- PathAlgebra
#              max_syzygy -- Integer that is greater than 0 used in Omega-periodicity check.

IsFractionalCalabiYau := function(kQ, max_syzygy)
  local triv_ext_alg, M; 
   if IsInt(max_syzygy) = false then
     Error("max_syzygy must be an integer.");
   fi;
   # We raise an error if kQ is not of type PathAlgebra
   if IsPathAlgebra(kQ) = false then
       Error("kQ must be a PathAlgebra.");
   else
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
   fi;
end;
