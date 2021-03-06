import numpy as np
import itertools as it
import db_functions as fn
import h5py
import time
import sys


tnum = np.int64(sys.argv[1])

filename = 'log_XtX_%s.txt' % str(tnum)

N_p = 215  # number of GSH bases to evaluate
N_q = 21  # number of cosine bases to evaluate
N_r = 10  # number of legendre bases to evaluate
cmax = N_p*N_q*N_r  # total number of permutations of basis functions
fn.WP(str(cmax), filename)

# iivec is vector of indices for all permutations of basis function indices
Ivec = np.arange(cmax)

# cmat is the matrix containing all permutations of basis function indices
cmat = np.unravel_index(np.arange(cmax), [N_p, N_q, N_r])
cmat = np.array(cmat).T

# indxmat is the matrix containing all unique combinations of elements of iivec
tmp = it.combinations_with_replacement(Ivec, 2)
Imat = np.array(list(tmp))
ImatL = Imat.shape[0]
fn.WP(str(ImatL), filename)

# pick range of indxmat to calculate
n_jobs = 200.  # number of jobs submitted to PACE
n_I = np.int64(np.ceil(np.float(ImatL)/n_jobs))  # number dot products per job
fn.WP(str(n_I), filename)

I_stt = tnum*n_I  # start index
if (tnum+1)*n_I > ImatL:
    I_end = ImatL
else:
    I_end = (tnum+1)*n_I  # end index

msg = "I_stt = %s" % I_stt
fn.WP(msg, filename)
msg = "I_end = %s" % I_end
fn.WP(msg, filename)

dotvec = np.zeros((I_end-I_stt, 3), dtype='complex128')

f = h5py.File('X_parts.hdf5', 'r')

c = 0
for I in xrange(I_stt, I_end):

    msg = str(I)
    fn.WP(msg, filename)

    ii, jj = Imat[I, :]
    iijj = np.array([ii, jj])
    fn.WP(str(iijj), filename)

    st = time.time()

    p, q, r = cmat[ii, :]
    basis_p = f.get('p_%s' % p)[...]
    basis_q = f.get('q_%s' % q)[...]
    basis_r = f.get('r_%s' % r)[...]
    ep_set_ii = basis_p*basis_q*basis_r

    p, q, r = cmat[jj, :]
    basis_p = f.get('p_%s' % p)[...]
    basis_q = f.get('q_%s' % q)[...]
    basis_r = f.get('r_%s' % r)[...]
    ep_set_jj = basis_p*basis_q*basis_r

    msg = "load time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    st = time.time()

    dotvec[c, 0:2] = iijj
    dotvec[c, 2] = np.dot(ep_set_ii.conj(), ep_set_jj)

    del ep_set_ii, ep_set_jj

    msg = "dot product time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    c += 1

f.close()

f = h5py.File('XtX%s.hdf5' % tnum, 'w')
f.create_dataset('dotvec', data=dotvec)
f.close()
