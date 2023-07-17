LoadPackage("qpa");

Q := Quiver(4, [[1, 2, "a"], [2, 4, "b"], [1, 3, "c"], [3, 4, "d"]]); 
pa := PathAlgebra(Rationals, Q); 
AssignGeneratorVariables(pa);

I := Ideal(pa, [a*b - c*d]);
quot := pa / I;
