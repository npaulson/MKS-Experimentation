import numpy as np
import gsh_hex_tri_L0_16 as gsh
import db_functions as fn
import h5py
import time


a = 0.0050
b = 0.0085
N_q = 16  # number of cosine bases to evaluate
L_th = np.pi/3.
filename = 'Xcalc_log.txt'

""" Load info from collected simulation info file """

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

theta = var_set[:, 0]

f.close

f = h5py.File('X_parts.hdf5', 'a')

""" second evalute the cosine basis functions """

st = time.time()

for q in xrange(N_q):

    # vec = np.cos(2.*np.pi*q*theta/L_th)
    vec = np.cos(q*np.pi*theta/L_th)

    set_id = 'q_%s' % q
    f.create_dataset(set_id, data=vec)
    fn.WP(set_id, filename)

msg = "Cosine basis evaluation complete: %ss" % np.round(time.time()-st, 3)
fn.WP(msg, filename)

f.close()
