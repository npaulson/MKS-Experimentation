import numpy as np
import itertools as it
import h5py
import time
import sys


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

tnum = np.int64(sys.argv[1])

filename = 'log_XtX_%s.txt' % str(tnum)

N_L = 15  # number of GSH basis functions
N_p = 8  # number of complex exponential basis functions
N_q = 8  # number of Legendre basis functions
cmax = N_L*N_p*N_q  # total number of permutations of basis functions
WP(str(cmax), filename)

# iivec is vector of indices for all permutations of basis function indices
Ivec = np.arange(cmax)

# cmat is the matrix containing all permutations of basis function indices
cmat = np.unravel_index(np.arange(cmax), [N_L, N_p, N_q])
cmat = np.array(cmat).T

# indxmat is the matrix containing all unique combinations of elements of iivec
tmp = it.combinations_with_replacement(Ivec, 2)
Imat = np.array(list(tmp))
ImatL = Imat.shape[0]
WP(str(ImatL), filename)

# pick range of indxmat to calculate
n_jobs = 50.  # number of jobs submitted to PACE
n_I = np.int64(np.ceil(np.float(ImatL)/n_jobs))  # number dot products per job
WP(str(n_I), filename)

I_stt = tnum*n_I  # start index
if (tnum+1)*n_I > ImatL:
    I_end = ImatL
else:
    I_end = (tnum+1)*n_I  # end index

msg = "I_stt = %s" % I_stt
WP(msg, filename)
msg = "I_end = %s" % I_end
WP(msg, filename)

dotvec = np.zeros((I_end-I_stt, 3), dtype='complex128')

c = 0
for I in xrange(I_stt, I_end):

    msg = str(I)
    WP(msg, filename)

    ii, jj = Imat[I, :]
    iijj = np.array([ii, jj])
    WP(str(iijj), filename)

    st = time.time()

    L, p, q = cmat[ii, :]
    set_id_ii = 'set_%s_%s_%s' % (L, p, q)
    f = h5py.File('pre_fourier_p%s_q%s.hdf5' % (p, q), 'r')
    ep_set_ii = f.get(set_id_ii)[...]
    f.close()

    L, p, q = cmat[jj, :]
    set_id_jj = 'set_%s_%s_%s' % (L, p, q)
    f = h5py.File('pre_fourier_p%s_q%s.hdf5' % (p, q), 'r')
    ep_set_jj = f.get(set_id_jj)[...]
    f.close()

    msg = "load time: %ss" % np.round(time.time()-st, 3)
    WP(msg, filename)

    st = time.time()

    dotvec[c, 0:2] = iijj
    dotvec[c, 2] = np.dot(ep_set_ii.conj(), ep_set_jj)

    del ep_set_ii, ep_set_jj

    msg = "dot product time: %ss" % np.round(time.time()-st, 3)
    WP(msg, filename)

    c += 1

f = h5py.File('XtX%s.hdf5' % tnum, 'w')
f.create_dataset('dotvec', data=dotvec)
f.close()
