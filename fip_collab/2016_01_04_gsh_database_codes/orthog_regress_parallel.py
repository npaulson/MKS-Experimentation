import numpy as np
import itertools as it
import db_functions as fn
import h5py
import time
import sys


tnum = np.int64(sys.argv[1])

filename = 'log_orthog_regress_parallel_%s.txt' % str(tnum)

""" Load Y vec """
f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')
Y = var_set[:, 5]
f.close

""" Initialize important variables """
N_p = 215  # number of GSH bases to evaluate
N_q = 21  # number of cosine bases to evaluate
N_r = 10  # number of legendre bases to evaluate

n_jobs = 50.  # number of jobs submitted to cluster

""" Calculate basis function indices """
cmax = N_p*N_q*N_r  # total number of permutations of basis functions
fn.WP(str(cmax), filename)

# cmat is the matrix containing all permutations of basis function indices
cmat = np.unravel_index(np.arange(cmax), [N_p, N_q, N_r])
cmat = np.array(cmat).T

""" Deal with the parallelization of this operation specifically pick range
of indxmat to calculate """
n_ii = np.int64(np.ceil(np.float(cmax)/n_jobs))  # number dot products per job
fn.WP(str(n_ii), filename)

ii_stt = tnum*n_ii  # start index
if (tnum+1)*n_ii > cmax:
    ii_end = cmax
else:
    ii_end = (tnum+1)*n_ii  # end index

msg = "ii_stt = %s" % ii_stt
fn.WP(msg, filename)
msg = "ii_end = %s" % ii_end
fn.WP(msg, filename)

""" perform the orthogonal regressions """

coeff_prt = np.zeros(ii_end-ii_stt, dtype='complex128')

f = h5py.File('X_parts.hdf5', 'r') 
c = 0

for ii in xrange(ii_stt, ii_end):

    msg = str(ii)
    fn.WP(msg, filename)

    st = time.time()

    p, q, r = cmat[ii, :]
    basis_p = f.get('p_%s' % p)[...]
    basis_q = f.get('q_%s' % q)[...]
    basis_r = f.get('r_%s' % r)[...]

    ep_set = np.squeeze(basis_p)*basis_q*basis_r

    msg = "load time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    st = time.time()

    XhYtmp = np.dot(ep_set.conj(), Y)
    XhXtmp = np.dot(ep_set.conj(), ep_set)
    del ep_set

    coeff_prt[c] = XhYtmp/XhXtmp

    msg = "regression time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    c += 1

f.close()

f = h5py.File('coeff_prt_%s.hdf5' % tnum, 'w')
f.create_dataset('coeff_prt', data=coeff_prt)
f.close()
