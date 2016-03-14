import numpy as np
import gsh_hex_tri_L0_16 as gsh
import db_functions as fn
import h5py
import time
import sys


tnum = np.int64(sys.argv[1])
filename = 'log_Xcalc_GSH_parallel_%s.txt' % str(tnum)

"""Initialize important variables"""

n_jobs = 40  # number of jobs submitted

LL_p = 16  # gsh truncation level
indxvec = gsh.gsh_basis_info()

# N_p: number of GSH bases to evaluate
N_p = np.sum(indxvec[:, 0] <= LL_p)
print N_p

""" Load info from collected simulation info file """

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

X = var_set[:, 1:4]  # contains phi1, phi and phi2
print X.nbytes/(1e9)

f.close

cmax = N_p

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

""" first evalute the GSH basis functions """

f = h5py.File('X_parts_GSH_%s.hdf5' % tnum, 'a')

for p in xrange(ii_stt, ii_end):

    st = time.time()

    vec = gsh.gsh_eval(X, [p])

    set_id = 'p_%s' % p
    f.create_dataset(set_id, data=vec)
    fn.WP(set_id, filename)

    msg = "GSH eval time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

f.close()
