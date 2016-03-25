import numpy as np
import gsh_cub_tri_L0_16 as gsh
import db_functions as fn
import h5py
import time
import sys
import constants


tnum = np.int64(sys.argv[1])
C = constants.const()
filename = 'log_basis_eval_gsh_%s.txt' % str(tnum).zfill(5)

""" Load info from collected simulation info file """

f = h5py.File(C['combineread_output'], 'r')
var_set = f.get('var_set')

g = np.zeros((C['n_eul'], 3), dtype='float64')
g[...] = var_set[:C['n_eul'], 1:4]

msg = "unique phi1: %s" % str(np.unique(g[:, 0])*(180/np.pi))
fn.WP(msg, filename)
msg = "unique Phi: %s" % str(np.unique(g[:, 1])*(180/np.pi))
fn.WP(msg, filename)
msg = "unique phi2: %s" % str(np.unique(g[:, 2])*(180/np.pi))
fn.WP(msg, filename)

f.close

""" Deal with the parallelization of this operation specifically pick range
of indxmat to calculate """

# n_ii: number of basis evaluations per job
n_ii = np.int64(np.ceil(np.float(C['N_p'])/C['basisgsh_njobs']))
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
# ch_len = np.int64(np.ceil(np.float(C['n_eul'])/C['basisgsh_nchunks']))

f = h5py.File(C['basisgsh_output'] % str(tnum).zfill(5), 'w')

for p in xrange(ii_stt, ii_end):

    st = time.time()

    vec = np.zeros(C['n_eul'], dtype='complex128')

    # for jj in xrange(C['basisgsh_nchunks']):
    #     jj_stt = jj*ch_len  # start index
    #     jj_end = jj_stt + ch_len
    #     if jj_end > C['n_eul']:
    #         jj_end = C['n_eul']

    #     tmp = gsh.gsh_eval(g[ii_stt:ii_end, :], [p])
    #     vec[ii_stt:ii_end] = np.squeeze(tmp)

    vec = np.squeeze(gsh.gsh_eval(g, [p]))

    set_id = 'p_%s' % str(p).zfill(5)
    f.create_dataset(set_id, data=vec)
    fn.WP(set_id, filename)

    msg = "GSH eval time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

f.close()

f_flag = open("flag%s" % str(tnum).zfill(5), 'w')
f_flag.close()
