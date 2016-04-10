# Definitions and Calculations of Symmetries in G
# 
restart;
with(LinearAlgebra):
with(linalg):
with(CodeGeneration);
with(StringTools):
with(ArrayTools):
interface(rtablesize = 200);
# 
index_final := ImportMatrix("index_final_L40.txt");
import1 := "import numpy as np\n\n\n"; funchead1 := "def gsh_basis_info():\n\n"; python_output := cat(import1, funchead1); python_output := cat(python_output, "    indxvec = np.array(["); tmp := convert(index_final[1, () .. ()], list); python_output := cat(python_output, "[", tmp[1], ", ", tmp[2], ", ", tmp[3], "]"); for indx from 2 to Size(index_final, 1) do tmp := convert(index_final[indx, () .. ()], list); python_output := cat(python_output, ",\n                        [", tmp[1], ", ", tmp[2], ", ", tmp[3], "]") end do; python_output := cat(python_output, "])\n\n", "    return indxvec\n\n\n"); print("index_final formated and added to python_output");
funchead2 := "def gsh_eval(X, Bvec):\n\n"; phisplit := "    phi1 = X[..., 2]\n    phi = X[..., 1]\n    phi2 = X[..., 0]\n\n"; phiiss := "    zvec = np.abs(phi) < 1e-8\n    zvec = zvec.astype(int)\n    randvec = np.round(np.random.rand(zvec.size)).reshape(zvec.shape)\n    randvecopp = np.ones(zvec.shape) - randvec\n    phi += (1e-7)*zvec*(randvec - randvecopp)\n\n"; initarray1 := "    final_shape = np.hstack([phi1.shape, len(Bvec)])\n"; initarray2 := "    tfunc = np.zeros(final_shape, dtype='complex128')\n\n"; python_output := cat(python_output, funchead2, phisplit, phiiss, initarray1, initarray2);
loopstart := "    c = 0\n    for Bindx in Bvec:\n\n"; python_output := cat(python_output, loopstart);
python_output := cat(python_output, "        c += 1\n\n"); python_output := cat(python_output, "    return tfunc\n"); autorun_str := "\n\nif __name__ == '__main__':\n    X = np.zeros([2, 3])\n    phi1 = np.array([0.1,0.2])\n    X[:, 0] = phi1\n    phi = np.array([0.0, 0.4])\n    X[:, 1] = phi\n    phi2 = np.array([0.3, 0.6])\n    X[:, 2] = phi2\n\n    indxvec = gsh_basis_info()\n    print indxvec\n\n    lte2 = indxvec[:, 0] <= 2\n    print lte2\n\n    Bvec = np.arange(indxvec.shape[0])[lte2]\n    print Bvec\n\n    out_tvalues = gsh_eval(X, Bvec)\n    print out_tvalues\n    print out_tvalues.shape\n"; print("all text added to python_output"); python_output := cat(python_output, autorun_str); python_output := SubstituteAll(python_output, "^", "**"); python_output := SubstituteAll(python_output, "(i)", "(1j)"); python_output := SubstituteAll(python_output, "*i", "*1j"); python_output := SubstituteAll(python_output, "exp", "np.exp"); python_output := SubstituteAll(python_output, "sqrt", "np.sqrt"); python_output := SubstituteAll(python_output, "cos", "np.cos"); python_output := SubstituteAll(python_output, "sin", "np.sin"); python_output := SubstituteAll(python_output, ";", ""); python_output := SubstituteAll(python_output, "blarg", "tfunc[..., c]"); print("all text converted to python syntax");
dir := currentdir();
file := cat(dir, "/template.py");
file := SubstituteAll(file, "/", "\\"); print(file);
fd := fopen(file, WRITE); fprintf(fd, "%s\n", python_output); fclose(fd);

