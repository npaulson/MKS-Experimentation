MKS 7th Order README
5/9/2014

### Serial Codes and Files ###
These codes perform the 1st, 2nd and 7th order calibration and
validation procedures of the MKS using serial techniques.
This was an attempt to reduce the memory usage for 7th order 
terms, but had the undesirable side effect of greatly reducing
the speed at which the codes ran.

Main Code:
main_serial.py
Support Code:
mks_functions_serial.py
Support Files:
FE_results_1001.npy
micr_1001.npy
resp_val.npy

### Original Method Codes ###
These codes perform the MKS calibration and validation procedures
with the use of the 7th order nearest neighbour terms. This uses
the original MKS structure where very little is saved to the
hard drive.

Main Code:
main_ord7.py
Support Code:
mks_functions_1001.py
Support Files:
FE_results_1001.npy
micr_1001.npy

### Plotting ###
These codes will plot strain field maps and strain histograms
for the results of the MKS and FE simulations

Main Code:
plot_resp_hist.py
Support Files:
mks_R_ord1_1001.npy
mks_R_ord2_1001.npy
mks_R_ord7_1001.npy
resp_val.npy
micr_1001.npy