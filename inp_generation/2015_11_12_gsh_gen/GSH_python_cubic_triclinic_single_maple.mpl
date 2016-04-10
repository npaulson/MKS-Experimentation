# Definitions and Calculations of Symmetries in G
# 
restart;
with(LinearAlgebra):
with(linalg):
with(CodeGeneration);
with(StringTools):
with(ArrayTools):
interface(rtablesize = 200);
P := (x,l,m,n) -> (((-1)^(l-m)*I^(n-m))/((2^l)*(l-m)!))*sqrt( ((l-m)!*(l+n)!)/((l+m)!*(l-n)!))*(1-cos(x))^(-(n-m)/2)*(1+cos(x))^(-(n+m)/2)*eval(diff((1-r)^(l-m)*(1+r)^(l+m),[r$(l-n)]),{r=cos(x)});
CubicRotationMatricies := {}:
interface(showassumed = 0 );
#assume(phi,RealRange(0,Pi)):assume(phi1,RealRange(0,2*Pi)):assume(phi2,RealRange(0,2*Pi)):
latticePositions := [1,2,3,-1,-2,-3]:
for idxOuterLattice in latticePositions do
for idxInnerLattice in latticePositions do
if abs(idxOuterLattice) = abs(idxInnerLattice) then 
next:
end:
latticeOrientationE1 := Vector(1..3);
latticeOrientationE3 := Vector(1..3);
latticeOrientationE1[abs(idxOuterLattice)] := sign(idxOuterLattice);
latticeOrientationE3[abs(idxInnerLattice)] := sign(idxInnerLattice);
latticeOrientationE2 := crossprod(latticeOrientationE3,latticeOrientationE1);
latticeOrientationE1 := transpose(Matrix(latticeOrientationE1));
latticeOrientationE2 := Matrix(latticeOrientationE2);
latticeOrientationE3 := transpose(Matrix(latticeOrientationE3));
CubicRotationMatricies := CubicRotationMatricies union {transpose(<latticeOrientationE1,latticeOrientationE2, latticeOrientationE3>)};
end:
end:
CubicRotationMatricies := convert(CubicRotationMatricies,list);
rotateE3 := (x) -> (< <cos(x),-sin(x),0> | <sin(x),cos(x), 0> | <0,0,1> >):
rotateE1 := (x) -> (< <1, 0, 0>|<0, cos(x), -sin(x)>|<0,sin(x),cos(x)> >):
rotateE2 := (x) -> (< <cos(x), 0, -sin(x)>|<0, 1, 0>|<sin(x),0,cos(x)> >):
rotateET3 := (x) -> (< <cos(x),sin(x),0> | <-sin(x),cos(x), 0> | <0,0,1> >):
rotateET1 := (x) -> (< <1, 0, 0>|<0, cos(x), sin(x)>|<0,-sin(x),cos(x)> >):
rotateET2 := (x) -> (< <cos(x), 0, sin(x)>|<0, 1, 0>|<-sin(x),0,cos(x)> >):

bungeRotation := (phi1,Phi,phi2) -> multiply(multiply(rotateE3(phi2), rotateE1(Phi)), rotateE3(phi1)):
SOKitRotation := (a,b,c) -> multiply(multiply(rotateET3(a), rotateE2(b)), rotateET3(c)):
B := bungeRotation(phi1+a,phi+b,phi2+c):
G := bungeRotation(phi1,phi,phi2);
RotationEquivs := []:
for cRotation in CubicRotationMatricies do
# Equivs := (  G  . Matrix(cRotation)):
Equivs := (Matrix(cRotation) . G):
II := B:
eqns := ({II[3,3] = Equivs[3,3], II[2,3]=Equivs[2,3], II[1,3] = Equivs[1,3], II[1,2] = Equivs[1,2], II[1,1] = Equivs[1,1], II[2,1] = Equivs[2,1], II[3,1] = Equivs[3,1], II[2,2] = Equivs[2,2], II[3,2] = Equivs[3,2]}):
solutions := allvalues(solve(eqns,[a,b,c]))[1]:
RotationEquivs := [RotationEquivs, solutions]:
#print("ROTATION-MATRIX------------------------------------------------------------------");
#print(cRotation);
#print("----------------------------Equivalent Euler Angle Operator");
#print(solutions);
end:
T := (phi1,phi,phi2,l,m,n) -> exp(I*m*phi2)*exp(I*n*phi1)*P(phi,l,m,n);
equivs := transpose(ArrayTools[Reshape](Matrix(convert(map((x) -> rhs(x), ListTools[Flatten](RotationEquivs)),vector)),[3,24])):
# Python(Matrix(eval(equivs)),optimize,resultname=TempExpr):
transpose(ArrayTools[Reshape](Matrix(convert(map((x) -> rhs(x), ListTools[Flatten](RotationEquivs)),vector)),[3,24]));
phi := 'phi': phi1 := 'phi1': phi2 := 'phi2':
dfunction := (s,n) -> piecewise(s=n, 1,0);
MyHandler := proc(operator,operands,default_value)
   # MyHandler issues a warning, clears the status flag and then
   # continues with the default value.
   #WARNING("division by zero in %1 with args %2",operator,operands);
   NumericStatus(division_by_zero = false);
if type(default_value,'float') then return 0.0 end if:
return 0;
end proc: 

getIndexed := (x) -> piecewise(type(x,'indexed'),x,type(x,'numeric'),1=1,op(map(getIndexed,convert(x,set))));
test_l := 21:
test_m := 0:
# 
# Solve for GSH Symmetry coefficients.
# 
eqnelement := (l,m,s,nu) -> seq(eval((T(phi1+equivs[nu,1],phi+equivs[nu,2],phi2+equivs[nu,3],l,s,n)-dfunction(s,n)),{phi=0,phi1=0,phi2=0}),n=-l..l):
pmat := (l,m) -> Matrix([seq(seq([eqnelement(l,m,s,nu)],s=-l..l),nu=1..24)]):

independent_sols := proc(index_l)
global pmat, eqnelement, getIndexed;
local l, p, free_parameters, ACoeffs, idx_eqn, weight, idx_inner, temp_sol, idx_A_Coefficient, ACoeffsT, orthoA;

p := pmat(index_l,0):
l := Matrix(LinearSolve(Matrix(p), ZeroVector(Dimension(p)[1]),free=t)):
free_parameters := convert(convert(map(getIndexed, convert(l,list)),set) minus {1=1},list):

# Is there at least one non-trivial solution?
#print(free_parameters);
if nops(free_parameters) < 1 and MatrixNorm(l,2) = 0 then
#print(l);
return false:
end if:
ACoeffs := Matrix((2*index_l+1),nops(free_parameters),(i,j) -> A[i,j]):

# Enumerate over all linearly independent solutions...
for idx_eqn from 1 to nops(free_parameters)
do
weight := [free_parameters[idx_eqn]=1]:
for idx_inner from 1 to nops(free_parameters)
do
if not (idx_eqn=idx_inner) then 
weight := [op(weight),free_parameters[idx_inner]=0];
end if:
end do:
temp_sol := eval(l, weight);
for idx_A_Coefficient from 1 to 2*index_l+1
do
ACoeffs[idx_A_Coefficient,idx_eqn] := temp_sol[idx_A_Coefficient,1]:
end do:
end do:

# Make the solutions mutually orthogonal
ACoeffsT := Matrix(transpose(ACoeffs));
orthoA := LinearAlgebra[GramSchmidt]([seq(ACoeffsT[ii],ii=1..nops(free_parameters))],normalized=true);
if nops(orthoA) = 1 then 
ACoeffs := Matrix(transpose(Matrix(orthoA))): 
else 
ACoeffs := Matrix(transpose(ArrayTools[Concatenate](1,seq(orthoA[ii],ii=1..nops(free_parameters))))): 
end if:

return Matrix(ACoeffs):
end proc:
# 
# 
generate_T_Function := proc(index_l, index_m, symmetry_coefficients)
local verifyMat, SymmetrizedT, real_symT, imag_symT, count_solutions, out_index, out_t_function, a, b, c;

verifyMat := (l,m) -> [[seq(T(phi1 ,phi,phi2,l,m,n),n=-l..l)]]:
if ts = false then return [[]], [[]]: end if:
#assume(a,real):assume(b,real):assume(c,real):
SymmetrizedT := Matrix(verifyMat(index_l,index_m)). symmetry_coefficients:
#SymmetrizedT := eval(Matrix(verifyMat(index_l,index_m)),{phi1=a,phi=b,phi2=c}) . symmetry_coefficients:
#real_symT := map((x) -> eval(eval(simplify(evalc(Re(x)))),{a=phi1,b=phi,c=phi2}),convert(SymmetrizedT,list)):
#imag_symT := map((x) -> eval(eval(simplify(evalc(Im(x)))),{a=phi1,b=phi,c=phi2}),convert(SymmetrizedT,list)):
count_solutions := Dimension(SymmetrizedT)[2]:
out_index := seq([index_l,index_m,index_nu],index_nu=1..count_solutions):
out_t_function := convert(transpose(Matrix([SymmetrizedT])),listlist):
return out_t_function, [out_index]:
end proc:

genTFunction := proc(l_set,bfunc)
local tfunction_index, tfunction_final, index_l, symmetry_coefficients, index_m, temp_final, temp_index, str_index_l, str_index_m, temp_out, coeff_temp, coeff_final, index_n, n_vals, index_final, coeff_id, c;
tfunction_index := []:
tfunction_final := [];
index_final := [];
coeff_id := [];
c = 0:

# Iterate over L values
for index_l in l_set
do

# Get Symmetry Coefficients...
symmetry_coefficients := independent_sols(index_l):

if symmetry_coefficients = false then
next:
end if:

for index_m from -index_l to index_l
do

temp_final, temp_index := generate_T_Function(index_l,index_m,symmetry_coefficients):

temp_index := Array(temp_index);

#print(temp_index);

# temp_final := Array(temp_final);
temp_final := Array((2*index_l+1)*temp_final);

n_vals := temp_index(1..-1,3);

for index_n from 1 to ArrayNumElems(n_vals)
do

# print(temp_index(index_n,1..-1));
# print(temp_final(index_n));

tfunction_final := [op(tfunction_final),[simplify(temp_final(index_n))]]:
index_final := [op(index_final), [temp_index(index_n,1..-1)]]:

end do:
end do:
print(index_l):
end do: 

return tfunction_final, index_final, coeff_id:

end proc:

start_l := 0; end_l := 4; l_set := [0, 1, 2, 3, 4]; tfunction_final, index_final, coeff_id := genTFunction(l_set);
print(Size(simplify(Matrix(tfunction_final))));
# 
