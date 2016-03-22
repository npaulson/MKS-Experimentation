import numpy as np
import gsh_hex_tri_L0_16 as gsh
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

X = np.zeros((var_set.shape[0], 3), dtype='float64')
X[:, 0] = var_set[:, 1]  # phi1
X[:, 1] = var_set[:, 2]  # phi
X[:, 2] = var_set[:, 3]  # phi2

f.close

""" Deal with the parallelization of this operation specifically pick range
of indxmat to calculate """

# n_ii: number dot products per job
n_ii = np.int64(np.ceil(np.float(C['N_p'])/C['XcalcGSH_njobs']))
fn.WP(str(n_ii), filename)

ii_stt = tnum*n_ii  # start index
if (tnum+1)*n_ii > C['N_p']:
    ii_end = C['N_p']
else:
    ii_end = (tnum+1)*n_ii  # end index

msg = "ii_stt = %s" % ii_stt
fn.WP(msg, filename)
msg = "ii_end = %s" % ii_end
fn.WP(msg, filename)

""" first evalute the GSH basis functions """

f = h5py.File(C['XcalcGSH_output'] % str(tnum).zfill(5), 'w')

for p in xrange(ii_stt, ii_end):

    st = time.time()

    vec = gsh.gsh_eval(X, [p])

    set_id = 'p_%s' % str(p).zfill(5)
    f.create_dataset(set_id, data=vec)
    fn.WP(set_id, filename)

    msg = "GSH eval time: %ss" % np.round(time.time()-st, 3)
    fn.WP(msg, filename)

f.close()

f_flag = open("flag%s" % str(tnum).zfill(5), 'w')
f_flag.close()
