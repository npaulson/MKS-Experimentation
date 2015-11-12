import numpy as np
import numpy.polynomial.legendre as leg
import gsh_hex_tri_L0_8 as gsh
import h5py


inc = 5  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

f = h5py.File('pre_fourier.hdf5', 'r+')
ep_set = f.get('ep_set')

theta = ep_set[:, 0]
e_angles = ep_set[:, 1:4]
et_norm = ep_set[:, 4]
Y = ep_set[:, 5]

L = (2.*np.pi)/3.
N_L = 15
N_p = 8
N_q = 8

dmax = N_L*N_p*N_q
X = np.zeros(theta.size, dmax)

d = 0
for L in xrange(N_L):
    for p in xrange(N_p):

        p_vec = np.zeros(N_p)
        p_vec[p] = 1

        for q in xrange(N_q):

            vec = gsh.gsh(e_angles) * \
                  leg.legval(et_norm, p_vec) * \
                  np.exp((1j*2*np.pi*q*theta)/L)

            set_id = 'set_%s_%s_%s' % (L, p, q)
            ep_set = f.create_dataset(set_id, data=vec)

f.close()
