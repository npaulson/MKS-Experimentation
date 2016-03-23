import numpy as np
import gsh_cub_tri_L0_16 as gsh
import db_functions as fn
import h5py
import time
import sys
import constants


tnum = np.int64(sys.argv[1])
C = constants.const()
filename = 'log_Xcalc_GSH_parallel_%s.txt' % str(tnum).zfill(5)

""" Load info from collected simulation info file """

f = h5py.File(C['combineread_output'], 'r')
var_set = f.get('var_set')

N_par = var_set.shape[0]
X = np.zeros((N_par, 3), dtype='float64')
X[:, 0] = var_set[:, 1]  # phi1
X[:, 1] = var_set[:, 2]  # phi
X[:, 2] = var_set[:, 3]  # phi2

f.close

""" Deal with the parallelization of this operation specifically pick range
of indxmat to calculate """

# n_ii: number of basis evaluations per job
n_ii = np.int64(np.ceil(np.float(C['N_p'])/C['XcalcGSH_njobs']))
fn.WP(str(n_ii), filename)

ii_stt = tnum*n_ii  # start index
ii_end = ii_stt + n_ii  # end index
if ii_end > ['N_p']:
    ii_end = ['N_p']

msg = "ii_stt = %s" % ii_stt
fn.WP(msg, filename)
msg = "ii_end = %s" % ii_end
fn.WP(msg, filename)

"""Evalute the GSH basis functions
I am chunking X into smaller pieces to reduce the memory burden"""

# ch_len: chunk lengths
ch_len = np.int64(np.ceil(np.float(N_par)/C['XcalcGSH_nchunks']))

f = h5py.File(C['XcalcGSH_output'] % str(tnum).zfill(5), 'w')

for p in xrange(ii_stt, ii_end):

    st = time.time()

    vec = np.zeros(N_par, dtype='complex128')

    for jj in xrange(C['XcalcGSH_nchunks']):
        jj_stt = jj*ch_len  # start index
        jj_end = jj_stt + ch_len
        if jj_end > N_par:
            jj_end = N_par

        tmp = gsh.gsh_eval(X[ii_stt:ii_end, :], [p])
        vec[ii_stt:ii_end] = np.squeeze(tmp)

    set_id = 'p_%s' % str(p).zfill(5)
    f.create_dataset(set_id, data=vec)
    fn.WP(set_id, filename)

    msg = "GSH eval time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

f.close()

f_flag = open("flag%s" % str(tnum).zfill(5), 'w')
f_flag.close()
