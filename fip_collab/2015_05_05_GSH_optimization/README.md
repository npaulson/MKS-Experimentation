The purpose of this code is to determine the accuracy of the MKS prediction given the removal of single GSH coefficients as local state descriptors

The code first runs without removing any coefficients, and then successively removes each coefficient up to the specified level (except for the 0th coefficient which is always 1 and must remain in the set)