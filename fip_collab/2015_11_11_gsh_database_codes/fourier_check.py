import numpy as np
import numpy.polynomial.legendre as leg
import gsh_hex_tri_L0_4 as gsh
import h5py
import time

"""
This script checks the accuracy of the predictions
of the calibrated fourier series approximating the
crystal plasticity solutions
"""

# define the number of increments for angular variables:

# n_p1 = 11  # number of phi1 samples
# n_P = 11  # number of Phi samples
# n_p2 = 11  # number of phi2 samples
# n_en = 100  # number of en samples

f_test = h5py.File('test_fourier.hdf5', 'r')
ep_set = f_test.get("ep_set")

theta = ep_set[:, 0]
e_angles = ep_set[:, 1:4]
et_norm = ep_set[:, 4]
Y = ep_set[:, 5]

f_coeff = h5py.File('fourier_coeff.hdf5', 'r')
coeff_vec = f_coeff.get('coeff_vec')

# N_L = np.max(coeff_vec[:,0])+1
# N_p = np.max(coeff_vec[:,1])+1
# N_q = np.max(coeff_vec[:,2])+1

interp_vec = np.zeros(ep_set.shape[0])

st = time.time()

for ii in xrange(coeff_vec.shape[0]):
    L, p, q = coeff_vec[ii, :3]

    p_vec = np.zeros(p+1)
    p_vec[p] = 1

    vec = gsh.gsh(e_angles, L) * \
        leg.legval(et_norm, p_vec) * \
        np.real(np.exp((1j*2*np.pi*q*theta)/L))

    interp_vec += vec

end = time.time()
n_interp = ep_set.shape[0]
time_per_interp = np.round((end-st)/n_interp, 7)

print "interpolation time per input set: %ss" % time_per_interp

error = np.abs(Y - interp_vec)*1E6

print "mean interpolation error: %s (ep in ppm)" % np.mean(error)
print "max interpolation error: %s (ep in ppm)" % np.max(error)

print "worst case prediction error:"
max_indx = np.argmax(error)
print "actual strain: %s" % Y[max_indx]
print "interpolated strain: %s" % interp_vec[max_indx]

f_test.close()
f_coeff.close()
