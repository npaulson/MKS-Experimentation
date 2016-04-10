# Definitions and Calculations of Symmetries in G
# 
restart:
with(LinearAlgebra):
with(linalg):
with(CodeGeneration):
with(StringTools):
with(ArrayTools):
interface(rtablesize = 200):
# 
start_index := 1; end_index := 10; tfunction_sim := ImportMatrix("tfunction_sim_L40.txt"):
print(Size(tfunction_sim)):
python_output := "":
for indx from start_index to end_index do python_output := cat(python_output, "        if Bindx == ", indx-1, ":\n"): sing_func_opt := eval(([codegen:-optimize])(tfunction_sim[indx], tryhard), pow = `^`): for indx2 to Size(sing_func_opt)[2]-1 do temp_str := Matlab([sing_func_opt[indx2]], output = string): python_output := cat(python_output, "            ", temp_str) end do: temp_str := Matlab(rhs(sing_func_opt[-1])[1], resultname = "blarg", output = string): python_output := cat(python_output, "            ", temp_str, "\n"): print(cat("t_function ", indx, " added to python_output")) end do:
python_output := SubstituteAll(python_output, "^", "**"): python_output := SubstituteAll(python_output, "(i)", "(1j)"): python_output := SubstituteAll(python_output, "*i", "*1j"): python_output := SubstituteAll(python_output, "exp", "np.exp"): python_output := SubstituteAll(python_output, "sqrt", "np.sqrt"): python_output := SubstituteAll(python_output, "cos", "np.cos"): python_output := SubstituteAll(python_output, "sin", "np.sin"): python_output := SubstituteAll(python_output, ";", ""): python_output := SubstituteAll(python_output, "blarg", "tfunc[..., c]"): print("all text converted to python syntax"):
file := cat("functions", start_index, "_", end_index, ".py"):
fd := fopen(file, WRITE): fprintf(fd, "%s\n", python_output): fclose(fd):

