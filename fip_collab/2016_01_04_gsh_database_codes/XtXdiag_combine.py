import numpy as np
import db_functions as fn
import h5py


filename = 'log_XtXcombine.txt'

N_p = 215  # number of GSH bases to evaluate
N_q = 21  # number of cosine bases to evaluate
N_r = 10  # number of legendre bases to evaluate
cmax = N_p*N_q*N_r  # total number of permutations of basis functions
print cmax

# XtX is the matrix (X^T * X) in the normal equation for multiple
# linear regression
XtX = np.zeros(cmax, dtype='complex128')

# pick range of indxmat to calculate
n_jobs = 50  # number of jobs submitted to PACE

c = 0
for tnum in xrange(n_jobs):

    fn.WP(str(tnum), filename)

    # load partially filled XtX arrays from each file
    f = h5py.File('XtX%s.hdf5' % tnum, 'r')
    dotvec = f.get('dotvec')

    for ii in xrange(dotvec.shape[0]):

        XtX[c] = dotvec[ii]
        c += 1


f = h5py.File('XtXtotal.hdf5', 'w')
f.create_dataset('XtX', data=XtX)
f.close()
