LoadPackage("qpa");

q := Quiver(3, [[1, 2, "a"], [2, 3, "b"]]);
field := Rationals;
pa := PathAlgebra(field, q);
