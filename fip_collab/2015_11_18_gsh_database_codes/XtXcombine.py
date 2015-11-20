import numpy as np
import h5py


def WP(msg, filename):
    """
    Summary:
        This function takes an input message and a filename, and appends that
        message to the file. This function also prints the message
    Inputs:
        msg (string): the message to write and print.
        filename (string): the full name of the file to append to.
    Outputs:
        both prints the message and writes the message to the specified file
    """
    fil = open(filename, 'a')
    print msg
    fil.write(msg)
    fil.write('\n')
    fil.close()

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

    WP(str(tnum), filename)

    # load partially filled XtX arrays from each file
    f = h5py.File('XtX%s.hdf5' % tnum, 'r')
    dotvec = f.get('dotvec')

    for c in xrange(dotvec.shape[0]):
        ii, jj = np.real(dotvec[c, 0:2])

        if XtX[ii, jj] != 0 and XtX[jj, ii] != 0:
            WP("overlap in parallel calculations!!!", filename)

        if ii == jj:
            XtX[ii, ii] = dotvec[c, 2]
        else:
            XtX[ii, jj] = dotvec[c, 2]
            XtX[jj, ii] = dotvec[c, 2]

f = h5py.File('XtXtotal.hdf5', 'w')
f.create_dataset('XtX', data=XtX)
f.close()
