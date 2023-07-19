Read("Functions.g");
Q := CreateQuiver(5);
kQ := PathAlgebra(Rationals, Q);

rels := LengthTwoRelations(kQ);
quot := CreateQuotientAlgebra(kQ, rels[1]);

result := IsFractionalCalabiYau(quot, 15);
Print(result);
Print("Total runtime:", StringTime(Runtime()));
