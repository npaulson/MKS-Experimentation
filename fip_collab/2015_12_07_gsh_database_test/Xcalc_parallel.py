import numpy as np
import numpy.polynomial.legendre as leg
import h5py
import time
import sys


p = np.int64(sys.argv[1])

f = h5py.File('pre_fourier.hdf5', 'r')
var_set = f.get('var_set')

et_norm = var_set[:, 0]

f.close

f = h5py.File('pre_fourier_p%s.hdf5' % p, 'a')

p_vec = np.zeros(p+1)
p_vec[p] = 1

st = time.time()

vec = leg.legval(et_norm, p_vec)

set_id = 'set_%s' % p
f.create_dataset(set_id, data=vec)

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)

f.close()
