import numpy as np
import numpy.polynomial.legendre as leg
import gsh_hex_tri_L0_4 as gsh
import h5py
import time


def WP(msg, filename):
    """
    Summary:
        This function takes an input message and a filename, and appends that
        message to the file. This function also prints the message
    Inputs:
        msg (string): the message to write and print.
        filename (string): the full name of the file to append to.
    Outputs:
        both prints the message and writes the message to the specified file
    """
    fil = open(filename, 'a')
    print msg
    fil.write(msg)
    fil.write('\n')
    fil.close()

filename = 'log_test_regression'

f = h5py.File('reg_coeff.hdf5', 'r')
coeff = f.get('coeff')[...]
f.close()

f = h5py.File('pre_fourier.hdf5', 'r')
var_set = f.get('var_set')

theta = var_set[:, 0]
phi1 = np.float64(var_set[:, 1])
phi = np.float64(var_set[:, 2])
phi2 = np.float64(var_set[:, 3])
et_norm = var_set[:, 4]
Y = var_set[:, 5]

f.close()

L_th = (2.*np.pi)/3.
N_L = 15
N_p = 8
N_q = 8
cmax = N_L*N_p*N_q

WP(str(theta.size), filename)
WP(str(cmax), filename)

cmat = np.unravel_index(np.arange(cmax), [N_L, N_p, N_q])
cmat = np.array(cmat).transpose()

st = time.time()

vec = np.zeros(theta.size, dtype='complex128')

for ii in xrange(cmax):
# for ii in xrange(10):

    if np.mod(ii, 100) == 0:
        WP(str(ii), filename)

    L, p, q = cmat[ii, :]

    p_vec = np.zeros(p+1)
    p_vec[p] = 1

    tmp = np.zeros(theta.size, dtype='complex128')

    tmp[:], null = gsh.gsh(phi1, phi, phi2, L)
    tmp[:] *= leg.legval(et_norm, p_vec)
    tmp[:] *= np.real(np.exp((1j*2.*np.pi*np.float(q)*theta)/L_th))
    tmp[:] *= coeff[ii]

    vec[:] += tmp

Ttime = np.round(time.time()-st, 3)
msg = "total interpolation time: %ss" % Ttime
WP(msg, filename)
msg = "interpolation time per point: %s" % (Ttime/theta.size)
WP(msg, filename)

msg = str(vec.shape)
WP(msg, filename)

error = np.abs(vec - Y)

msg = "mean error: %s" % np.mean(error)
WP(msg, filename)
msg = "std of error: %s" % np.std(error)
WP(msg, filename)
msg = "min error: %s" % np.min(error)
WP(msg, filename)

f = h5py.File('regression_results.hdf5', 'w')
# results = f.create_dataset("results", (Y.size, 8))

results = np.zeros((Y.size, 8), dtype='complex128')
results[:, 0] = theta
results[:, 1] = phi1
results[:, 2] = phi
results[:, 3] = phi2
results[:, 4] = et_norm
results[:, 5] = Y
results[:, 6] = vec
results[:, 7] = error
f.create_dataset('results', data=results)
f.close()
