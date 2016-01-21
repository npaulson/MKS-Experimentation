import numpy as np
import db_functions as fn
import h5py
import time
import sys


tnum = np.int64(sys.argv[1])

filename = 'log_integrate_parallel_%s.txt' % str(tnum)

""" Load Y vec """
f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')
Y = var_set[:, 1]
f.close

""" Initialize important variables """

# these indices are defined for the sampled db inputs
inc = 6  # degree increment for angular variables
sub2rad = inc*np.pi/180.

n_th = 60/inc  # number of theta samples for FZ

N_q = 16  # number of cosine bases to evaluate

L_th = np.pi/3.

n_jobs = 5.  # number of jobs submitted to cluster

""" Calculate basis function indices """
cmax = N_q  # total number of permutations of basis functions
fn.WP(str(cmax), filename)

# cmat is the matrix containing all permutations of basis function indices
cmat = np.arange(cmax)

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

bsz_cos = L_th/n_th

for ii in xrange(ii_stt, ii_end):

    msg = str(ii)
    fn.WP(msg, filename)

    st = time.time()

    q = cmat[ii]
    basis_q = f.get('q_%s' % q)[...]

    ep_set = basis_q

    msg = "load time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    st = time.time()

    c_cos = 2./L_th

    c_tot = c_cos*bsz_cos

    tmp = c_tot*np.sum(Y*ep_set.conj())

    del ep_set

    coeff_prt[c] = tmp

    msg = "regression time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

    c += 1

f.close()

f = h5py.File('coeff_prt_%s.hdf5' % tnum, 'w')
f.create_dataset('coeff_prt', data=coeff_prt)
f.close()
