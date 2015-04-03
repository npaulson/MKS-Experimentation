# Definitions and Calculations of Symmetries in G
# 
# 
restart;
with(LinearAlgebra):
with(linalg):
with(CodeGeneration);
with(StringTools):
interface(rtablesize = 20);
P := (x,l,m,n) -> (((-1)^(l-m)*I^(n-m))/((2^l)*(l-m)!))*sqrt( ((l-m)!*(l+n)!)/((l+m)!*(l-n)!))*(1-cos(x))^(-(n-m)/2)*(1+cos(x))^(-(n+m)/2)*eval(diff((1-r)^(l-m)*(1+r)^(l+m),[r$(l-n)]),{r=cos(x)});

HexagonalRotationMatricies := {}:
interface(showassumed = 0 );
#assume(phi,RealRange(0,Pi)):assume(phi1,RealRange(0,2*Pi)):assume(phi2,RealRange(0,2*Pi)):
# This is an orientation matrix (sample to crystal) given some axis angle pair (theta and [u,v,w])
g_test := proc (theta, u, v, w) options operator, arrow; Matrix(1 .. 3, 1 .. 3, {(1, 1) = cos(theta)+u^2*(1-cos(theta)), (1, 2) = u*v*(1-cos(theta))+w*sin(theta), (1, 3) = u*w*(1-cos(theta))-v*sin(theta), (2, 1) = u*v*(1-cos(theta))-w*sin(theta), (2, 2) = cos(theta)+v^2*(1-cos(theta)), (2, 3) = v*w*(1-cos(theta))+u*sin(theta), (3, 1) = u*w*(1-cos(theta))+v*sin(theta), (3, 2) = v*w*(1-cos(theta))-u*sin(theta), (3, 3) = cos(theta)+w^2*(1-cos(theta))}, datatype = anything, storage = rectangular, order = Fortran_order, subtype = Matrix) end proc;
# Here we generate the hexagonal symmetry operators for the 622 point group
HexagonalRotationMatricies := {}; for ii from 0 to 5 do HexagonalRotationMatricies := `union`(HexagonalRotationMatricies, {g_test((1/3)*Pi*ii, 0, 0, 1)}) end do; HexagonalRotationMatricies := `union`(HexagonalRotationMatricies, {g_test(Pi, 1, 0, 0)}); HexagonalRotationMatricies := `union`(HexagonalRotationMatricies, {g_test(Pi, 1/2, (1/2)*sqrt(3), 0)}); HexagonalRotationMatricies := `union`(HexagonalRotationMatricies, {g_test(Pi, 1/2, (-sqrt(3))*(1/2), 0)}); HexagonalRotationMatricies := `union`(HexagonalRotationMatricies, {g_test(Pi, 0, 1, 0)}); HexagonalRotationMatricies := `union`(HexagonalRotationMatricies, {g_test(Pi, (1/2)*sqrt(3), 1/2, 0)}); HexagonalRotationMatricies := `union`(HexagonalRotationMatricies, {g_test(Pi, (1/2)*sqrt(3), -1/2, 0)}); HexagonalRotationMatricies := convert(HexagonalRotationMatricies, list);
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
for cRotation in HexagonalRotationMatricies do
Equivs := (  G  . Matrix(cRotation)):
II := B:
eqns := ({II[3,3] = Equivs[3,3], II[2,3]=Equivs[2,3], II[1,3] = Equivs[1,3], II[1,2] = Equivs[1,2], II[1,1] = Equivs[1,1], II[2,1] = Equivs[2,1], II[3,1] = Equivs[3,1], II[2,2] = Equivs[2,2], II[3,2] = Equivs[3,2]}):
solutions := allvalues(solve(eqns,[a,b,c]))[1]:
RotationEquivs := [RotationEquivs, solutions]:
#print("ROTATION-MATRIX------------------------------------------------------------------");
#print(cRotation);
#print("----------------------------Equivalent Euler Angle Operator");
#print(solutions);
end:
T := (phi1,phi,phi2,l,m,n) -> exp(I*m*phi1)*exp(I*n*phi2)*P(phi,l,m,n);
equivs := transpose(ArrayTools[Reshape](Matrix(convert(map((x) -> rhs(x), ListTools[Flatten](RotationEquivs)),vector)),[3,12]));
CodeGeneration['Matlab'](Matrix(eval(equivs)),optimize,resultname=TempExpr):
transpose(ArrayTools[Reshape](Matrix(convert(map((x) -> rhs(x), ListTools[Flatten](RotationEquivs)),vector)),[3,12])):
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
pmat := (l,m) -> Matrix([seq(seq([eqnelement(l,m,s,nu)],s=-l..l),nu=1..12)]):

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
return [out_t_function, [out_index]]:
end proc:

genTFunction := proc(start_l,end_l)
local tfunction_index, tfunction_final, index_l, symmetry_coefficients, index_m, temp_final, temp_index, str_index_l, str_index_m, str_index_nu, str_function, matlab_output, fd, count_solutions, temp_out, header, block1, block2, indx, temp_str, mat_indx;
tfunction_index := []:
tfunction_final := [];

# Iterate over L values
for index_l from  start_l to end_l
do

# Get Symmetry Coefficients...
symmetry_coefficients := independent_sols(index_l):

if symmetry_coefficients = false then
next:
end if:

#stopwhen(tfunction_final);
for index_m from -index_l to index_l
do
temp_out := generate_T_Function(index_l,index_m,symmetry_coefficients):
temp_index := op(temp_out[2]):
temp_final := temp_out[1]:
#print(op(temp_final));
#print(op(map( x-> seq([x*simplify(ChebyshevT(ii,theta))],ii=1..1),op(temp_final))));
#tfunction_index := [op(tfunction_index),temp_index]:
tfunction_final := [op(tfunction_final),op(temp_final)]:
#tfunction_final := [op(tfunction_final),op(map( x-> seq([x*simplify(ChebyshevT(ii,theta))],ii=0..2),op(temp_final)))]:
end do:
end do: 

# print(tfunction_index):
# print(Matrix(tfunction_final));

header := cat("function [out_tvalues]=gsh_hexagonal_triclinic_L", start_l, "_", end_l, "(phi1, phi, phi2)\n\n");
block1 := "zvec = abs(phi) < 10e-17;\nrandvec = round(rand(size(zvec)));\nrandvecopp = ones(size(zvec)) - randvec;\nphi = phi + (1e-7)*zvec.*(randvec - randvecopp);\n\n";
block2 := cat("out_tvalues = zeros(", nops(tfunction_final), ", length(phi1));\n\n"):
matlab_output  := cat(header, block1, block2):

for indx from 1 to nops(tfunction_final)
do

temp_str := Matlab(tfunction_final[indx][1], resultname = "out_tvalues", output = string):
mat_indx := cat("(", indx, ", :)"):
temp_str := Insert(temp_str, 11, mat_indx):
matlab_output := cat(matlab_output, temp_str):

end do:

return matlab_output, tfunction_final:

end proc:
# 
# Find independent solutions for L=4 for hexagonal symmetry. 
sys := independent_sols(4);
# Analytical Expression for the harmonics for L=-4 to L=4 ...
a := [generate_T_Function(4,-4,sys)[1][1][1]];
# 
# Generate Matlab code in c:\\gsh_tt_hexagonal_triclinic_0_4.m
start_l := 0:
end_l := 4:
matlab_output, tfunction_final := genTFunction(start_l, end_l):
#file := cat("C:/Users/nhpnp3/Documents/MKS-Experimentation/inp_generation/03_01_2015_gsh_gen/gsh_hexagonal_triclinic_L",start_l,"_",end_l,".m"):
#fd := fopen(file, WRITE):
fd := fopen('test.m', WRITE):
fprintf(fd, "%s\n", matlab_output):
fclose(fd):

mmm := evalf(eval(Matrix(tfunction_final), [phi1 = .1, phi = .2, phi2 = .3]));
print(tfunction_final):
print(matlab_output):



# 
