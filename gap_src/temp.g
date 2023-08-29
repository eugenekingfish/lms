Read("Functions.g");
Read("FCY.g");

QQ := CreateQuiver(6);
kQQ := PathAlgebra(Rationals, QQ);

Q := Quiver(6, [[1,2,"a1"], [2,3,"a2"], [3,4, "a3"], [4,5,"a4"], [5,6,"a5"], [3,1,"b12"], [5,2,"b234"], [6,4,"b45"]]);
kQ := PathAlgebra(Rationals, Q);

rels := [kQ.a1 * kQ.a2 * kQ.a3, kQ.a3 * kQ.a4 * kQ.a5]; # default relations 
Append(rels, [kQ.b45 * kQ.a4 * kQ.b234, kQ.b234 * kQ.a2 * kQ.b12]); # square free 
Append(rels, [kQ.a5 * kQ.b45 - kQ.b234 * kQ.a2 * kQ.a3, kQ.a3 * kQ.a4 * kQ.b234 - kQ.b12 * kQ.a1]); # overlap

Q_te := CreateQuotientAlgebra(kQ, rels);
proj_mods := IndecProjectiveModules(Q_te);
#te := TrivialExtensionOfQuiverAlgebra(kQQ);
