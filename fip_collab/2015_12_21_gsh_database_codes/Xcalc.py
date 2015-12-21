import numpy as np
import numpy.polynomial.legendre as leg
import gsh_hex_tri_L0_4 as gsh
import db_functions as fn
import h5py
import time


a = 0.0050
b = 0.0085
N_p = 215  # number of GSH bases to evaluate
N_q = 21  # number of cosine bases to evaluate
N_r = 10  # number of legendre bases to evaluate
L_th = (2.*np.pi)/3.
filename = 'Xcalc_log.txt'

""" Load info from collected simulation info file """

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

theta = var_set[:, 0]

X = np.zeros((theta.size, 3), dtype='float64')
X[:, 0] = var_set[:, 1]  # phi1
X[:, 1] = var_set[:, 2]  # phi
X[:, 2] = var_set[:, 3]  # phi2

et_norm = var_set[:, 4]

f.close


f = h5py.File('X_parts.hdf5', 'a')

""" first evalute the GSH basis functions """

st = time.time()

for p in xrange(N_p):

    vec = gsh.gsh(X, [p])

    set_id = 'p_%s' % p
    f.create_dataset(set_id, data=vec)

msg = "GSH basis evaluation complete: %ss" % np.round(time.time()-st, 3)
fn.WP(msg, filename)

""" second evalute the cosine basis functions """

st = time.time()

for q in xrange(N_q):

    vec = np.cos(2.*np.pi*q*theta/L_th)

    set_id = 'q_%s' % q
    f.create_dataset(set_id, data=vec)

msg = "Cosine basis evaluation complete: %ss" % np.round(time.time()-st, 3)
fn.WP(msg, filename)

""" third evalute the legendre basis functions """

st = time.time()

for r in xrange(N_r):

    r_vec = np.zeros(r+1)
    r_vec[r] = 1

    vec = leg.legval(et_norm, r_vec)

    set_id = 'r_%s' % r
    f.create_dataset(set_id, data=vec)

msg = "Legendre basis evaluation complete: %ss" % np.round(time.time()-st, 3)
fn.WP(msg, filename)

f.close()
