import numpy as np
import db_functions as fn
import h5py
import time


filename = 'log_XtY.txt'

N_p = 215  # number of GSH bases to evaluate
N_q = 21  # number of cosine bases to evaluate
N_r = 10  # number of legendre bases to evaluate
cmax = N_p*N_q*N_r  # total number of permutations of basis functions
cvec = np.unravel_index(np.arange(cmax), [N_L, N_p, N_q])
cvec = np.array(cvec).T

st = time.time()

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')
Y = var_set[:, 5]
f.close

XtY = np.zeros(cmax, dtype='complex128')

f = h5py.File('X_parts.hdf5', 'r')

for ii in xrange(cmax):

    fn.WP(str(ii), filename)

    p, q, r = cvec[ii, :]
    basis_p = f.get('p_%s' % p)[...]
    basis_q = f.get('q_%s' % q)[...]
    basis_r = f.get('r_%s' % r)[...]
    ep_set_ii = basis_p*basis_q*basis_r

    XtY[ii] = np.dot(ep_set_ii.conj(), Y)

f.close()

f = h5py.File('XtYtotal.hdf5', 'w')
f.create_dataset('XtY', data=XtY)
f.close()

fn.WP("XtY prepared: %ss" % (np.round(time.time()-st, 3)), filename)
