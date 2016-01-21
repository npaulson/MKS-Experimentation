import numpy as np
import gsh_hex_tri_L0_16 as gsh
import db_functions as fn
import h5py
import time


a = 0.0050
b = 0.0085
N_p = 215  # number of GSH bases to evaluate
filename = 'Xcalc_log.txt'

""" Load info from collected simulation info file """

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

X = np.zeros((var_set.shape[0], 3), dtype='float64')
X[:, 0] = var_set[:, 0]  # phi1
X[:, 1] = var_set[:, 1]  # phi
X[:, 2] = var_set[:, 2]  # phi2

f.close


f = h5py.File('X_parts.hdf5', 'a')

""" first evalute the GSH basis functions """

st = time.time()

for p in xrange(N_p):

    vec = gsh.gsh_eval(X, [p])

    set_id = 'p_%s' % p
    f.create_dataset(set_id, data=vec)
    fn.WP(set_id, filename)


msg = "GSH basis evaluation complete: %ss" % np.round(time.time()-st, 3)
fn.WP(msg, filename)

f.close()
