import numpy as np
import db_functions as fn
import h5py
import time


a = 0.00485  # start for en range
b = 0.00905  # end for en range

N_q = 40  # number of cosine bases to evaluate for theta
N_r = 14  # number of cosine bases to evaluate for en

L_th = np.pi/3.
L_en = b-a
filename = 'Xcalc_log_cos.txt'

""" Load info from collected simulation info file """

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

theta = var_set[:, 0]
et_norm = var_set[:, 4]

f.close

f = h5py.File('X_parts_cos.hdf5', 'a')

"""Evalute the cosine basis functions for theta"""

st = time.time()

for q in xrange(N_q):

    vec = np.cos(q*np.pi*theta/L_th)

    set_id = 'q_%s' % q
    f.create_dataset(set_id, data=vec)
    fn.WP(set_id, filename)

msg = "Cosine basis evaluation for theta complete: %ss" \
    % np.round(time.time()-st, 3)
fn.WP(msg, filename)

"""Evalute the cosine basis functions for en"""

st = time.time()

for r in xrange(N_r):

    vec = np.cos(r*np.pi*(et_norm-a)/L_en)

    set_id = 'r_%s' % r
    f.create_dataset(set_id, data=vec)
    fn.WP(set_id, filename)

msg = "Cosine basis evaluation for en complete: %ss" \
    % np.round(time.time()-st, 3)
fn.WP(msg, filename)

f.close()
