import numpy as np
import db_functions as fn
import h5py
import time

N_q = 60  # number of cosine bases to evaluate for theta

L_th = np.pi/3.
filename = 'Xcalc_cos_log.txt'

""" Load info from collected simulation info file """

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

theta = var_set[:, 0]
print theta.nbytes/(1e9)

f.close

f = h5py.File('X_parts_cos.hdf5', 'a')

"""evalute the cosine basis functions for theta"""

st = time.time()

for q in xrange(N_q):

    vec = np.cos(q*np.pi*theta/L_th)

    set_id = 'q_%s' % q
    f.create_dataset(set_id, data=vec)
    fn.WP(set_id, filename)

msg = "Cosine basis evaluation for theta complete: %ss" \
    % np.round(time.time()-st, 3)
fn.WP(msg, filename)

f.close()
