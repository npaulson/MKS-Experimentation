import numpy as np
import numpy.polynomial.legendre as leg
import gsh_hex_tri_L0_4 as gsh
import h5py
import time
import sys


p = np.int8(sys.argv[1])
q = np.int8(sys.argv[2])

f = h5py.File('pre_fourier.hdf5', 'r')
ep_set = f.get('ep_set')

theta = ep_set[:, 0]
phi1 = np.float64(ep_set[:, 1])
phi = np.float64(ep_set[:, 2])
phi2 = np.float64(ep_set[:, 3])
et_norm = ep_set[:, 4]

f.close

f = h5py.File('pre_fourier_p%s_q%s.hdf5' % (p, q), 'a')

L_th = (2.*np.pi)/3.
p_vec = np.zeros(p+1)
p_vec[p] = 1
N_L = 15

st = time.time()

for L in xrange(N_L):

    vec, cmat = gsh.gsh(phi1, phi, phi2, L)
    vec *= leg.legval(et_norm, p_vec)
    vec *= np.real(np.exp((1j*2.*np.pi*np.float(q)*theta)/L_th))

    set_id = 'set_%s_%s_%s' % (L, p, q)
    f.create_dataset(set_id, data=vec)

    tmp = np.array([L, p, q])
    print tmp

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)

f.close()
