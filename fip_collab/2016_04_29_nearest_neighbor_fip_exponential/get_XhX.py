import numpy as np
import functions as rr
from constants import const
import h5py
import time
import sys


st = time.time()

tnum = np.int64(sys.argv[1])
C = const()
log_file = 'log_XhX_%s.txt' % tnum

"""import X"""
f = h5py.File("pre_regress_%s.hdf5" % C['set_id_cal'], 'r')
X = f.get('X')[...]
f.close()

"""Deal with the parallelization of this operation specifically pick range
of indxmat to calculate"""

# n_ii: number of basis evaluations per job
n_ii = np.int64(np.ceil(np.float(C['ImatL'])/C['XhX_njobs']))
msg = "number of dot products per job: %s" % n_ii
rr.WP(msg, log_file)

ii_stt = tnum*n_ii  # start index
ii_end = ii_stt + n_ii  # end index
if ii_end > C['ImatL']:
    ii_end = C['ImatL']

msg = "ii_stt = %s" % ii_stt
rr.WP(msg, log_file)
msg = "ii_end = %s" % ii_end
rr.WP(msg, log_file)

"""calculate the components in XhX for ii_stt to ii_end"""

f = h5py.File("XhX_%s.hdf5" % str(tnum).zfill(5), 'w')
XhXvec = f.create_dataset("XhXvec", (ii_end-ii_stt, 3), dtype='float64')

c = 0
for I in xrange(ii_stt, ii_end):

    if np.mod(I, 10000) == 0:
        rr.WP(str(I), log_file)

    ii, jj = C['Imat'][I, :]
    dotvec = np.dot(X[:, ii], X[:, jj])
    XhXvec[c, :] = np.array([ii, jj, dotvec])
    c += 1

f.close()

timeE = np.round(time.time()-st, 1)
msg = "XhX job #%s: %s s" % (tnum, timeE)
rr.WP(msg, log_file)

f_flag = open("flag%s" % str(tnum).zfill(5), 'w')
f_flag.close()
