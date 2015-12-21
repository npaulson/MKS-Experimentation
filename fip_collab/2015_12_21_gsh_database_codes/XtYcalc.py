import numpy as np
import db_functions as fn
import h5py
import time


filename = 'log_XtY.txt'

N_L = 15
N_p = 8
N_q = 8
cmax = N_L*N_p*N_q
cvec = np.unravel_index(np.arange(cmax), [N_L, N_p, N_q])
cvec = np.array(cvec).T

st = time.time()

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')
Y = var_set[:, 5]
f.close

XtY = np.zeros(cmax, dtype='complex128')

for ii in xrange(cmax):

    fn.WP(str(ii), filename)

    L, p, q = cvec[ii, :]
    set_id_ii = 'set_%s_%s_%s' % (L, p, q)
    f = h5py.File('pre_fourier_p%s_q%s.hdf5' % (p, q), 'r')
    ep_set_ii = f.get(set_id_ii)[...]
    f.close()

    XtY[ii] = np.dot(ep_set_ii.conj(), Y)

f = h5py.File('XtYtotal.hdf5', 'w')
f.create_dataset('XtY', data=XtY)
f.close()

fn.WP("XtY prepared: %ss" % (np.round(time.time()-st, 3)), filename)
