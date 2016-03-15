import numpy as np
import gsh_cub_tri_L0_16 as gsh
import db_functions as fn
import h5py
import time
import sys


tnum = np.int64(sys.argv[1])
filename = 'log_Xcalc_GSH_parallel_%s.txt' % str(tnum)

"""Initialize important variables"""

n_jobs = 15  # number of jobs submitted
n_chunks = 100  # number of chunks to split X into to reduce memory usage

LL_p = 16  # gsh truncation level
indxvec = gsh.gsh_basis_info()

# N_p: number of GSH bases to evaluate
N_p = np.sum(indxvec[:, 0] <= LL_p)
print N_p

""" Load info from collected simulation info file """

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

X = var_set[:, 1:4]  # contains phi1, phi and phi2
N_par = X.shape[0]

print X.nbytes/(1e9)

f.close

cmax = N_p

""" Deal with the parallelization of this operation specifically pick range
of indxmat to calculate """
n_ii = np.int64(np.ceil(np.float(cmax)/n_jobs))  # number evaluations per job
fn.WP(str(n_ii), filename)

ii_stt = tnum*n_ii  # start index
ii_end = ii_stt + n_ii  # end index
if ii_end > cmax:
    ii_end = cmax

msg = "ii_stt = %s" % ii_stt
fn.WP(msg, filename)
msg = "ii_end = %s" % ii_end
fn.WP(msg, filename)

"""Evalute the GSH basis functions
I am chunking X into smaller pieces to reduce the memory burden"""

ch_len = np.int64(np.ceil(np.float(N_par)/n_chunks))  # chunk lengths

f = h5py.File('X_parts_GSH_%s.hdf5' % tnum, 'a')

for p in xrange(ii_stt, ii_end):

    st = time.time()

    vec = np.zeros(X.shape[0], dtype='complex128')

    for jj in xrange(n_chunks):
        jj_stt = jj*ch_len  # start index
        jj_end = jj_stt + ch_len
        if jj_end > N_par:
            jj_end = N_par

        tmp = gsh.gsh_eval(X[ii_stt:ii_end, :], [p])
        vec[ii_stt:ii_end] = np.squeeze(tmp)

    set_id = 'p_%s' % p
    f.create_dataset(set_id, data=vec)
    fn.WP(set_id, filename)

    msg = "GSH eval time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

f.close()
