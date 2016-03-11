import numpy as np
import gsh_hex_tri_L0_16 as gsh
import db_functions as fn
import h5py
import time


LL_p = 16  # gsh truncation level
indxvec = gsh.gsh_basis_info()

# N_p: number of GSH bases to evaluate
N_p = np.sum(indxvec[:, 0] <= LL_p)
print N_p

""" Load info from collected simulation info file """

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

X = var_set[:, 1:4]  # contains phi1, phi and phi2

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
