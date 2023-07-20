Read("Functions.g");

fn := "outputs/output6.txt";
n := 6;
AppendTo(fn, "n = ", n, "\n\n");

Q := CreateQuiver(n);
kQ := PathAlgebra(Rationals, Q);
rels := LengthTwoRelations(kQ);

for i in [2..Length(rels)] do
   AppendTo(fn, rels[i], " --- ");
  Print("Checking: ", rels[i], "\n");
  quot := CreateQuotientAlgebra(kQ, rels[i]);
  result := IsFractionalCalabiYau(quot, 20);
  AppendTo(fn, result, "\n");
od;
Print("FINISHED.\n");
quit;
