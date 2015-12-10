import numpy as np
import db_functions as fn
import h5py


filename = 'log_XtXcombine.txt'

N_L = 15  # number of GSH basis functions
N_p = 8  # number of complex exponential basis functions
N_q = 8  # number of Legendre basis functions
cmax = N_L*N_p*N_q  # total number of permutations of basis functions
print cmax

# XtX is the matrix (X^T * X) in the normal equation for multiple
# linear regression
XtX = np.zeros((cmax, cmax), dtype='complex128')

# pick range of indxmat to calculate
n_jobs = 50  # number of jobs submitted to PACE

for tnum in xrange(n_jobs):

    fn.WP(str(tnum), filename)

    # load partially filled XtX arrays from each file
    f = h5py.File('XtX%s.hdf5' % tnum, 'r')
    dotvec = f.get('dotvec')

    for c in xrange(dotvec.shape[0]):
        ii, jj = np.real(dotvec[c, 0:2])

        if XtX[ii, jj] != 0 and XtX[jj, ii] != 0:
            fn.WP("overlap in parallel calculations!!!", filename)

        if ii == jj:
            XtX[ii, ii] = dotvec[c, 2]
        else:
            XtX[ii, jj] = dotvec[c, 2]
            XtX[jj, ii] = dotvec[c, 2]

msg = "rank(XtX): %s" % np.linalg.matrix_rank(XtX)
fn.WP(msg, filename)

f = h5py.File('XtXtotal.hdf5', 'w')
f.create_dataset('XtX', data=XtX)
f.close()
