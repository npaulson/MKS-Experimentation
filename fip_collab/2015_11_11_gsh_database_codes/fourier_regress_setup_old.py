import numpy as np
import numpy.polynomial.legendre as leg
import gsh_hex_tri_L0_4 as gsh
import h5py
import time

 = sys.argv[1]


f = h5py.File('pre_fourier.hdf5', 'r')
ep_set = f.get('ep_set')

theta = ep_set[:, 0]
e_angles = ep_set[:, 1:4]
et_norm = ep_set[:, 4]
# Y = ep_set[:, 5]

f.close

f = h5py.File('pre_fourier_vec.hdf5', 'w')

L_th = (2.*np.pi)/3.
N_L = 15
N_p = 8
N_q = 8

cmax = N_L*N_p*N_q
cvec = np.zeros([cmax, 3])

st = time.time()

for c in xrange(cmax):

    [L, p, q] = np.unravel_index(c, [N_L, N_p, N_q])

    p_vec = np.zeros(N_p)
    p_vec[p] = 1

    vec, cmat = gsh.gsh(np.transpose(e_angles), L)
    vec *= leg.legval(et_norm, p_vec)
    vec *= np.real(np.exp((1j*2.*np.pi*np.float(q)*theta)/L_th))

    set_id = 'set_%s_%s_%s' % (L, p, q)
    f.create_dataset(set_id, data=vec)

    tmp = np.array([L, p, q])
    print tmp
    cvec[c, :] = tmp

f.create_dataset('cvec', data=cvec)

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)

f.close()
