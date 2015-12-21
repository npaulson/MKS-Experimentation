import numpy as np
import numpy.polynomial.legendre as leg
import gsh_hex_tri_L0_4 as gsh
import db_functions as fn
import h5py
import time


a = 0.0050
b = 0.0085
filename = 'log_test_regression.txt'

f = h5py.File('reg_coeff.hdf5', 'r')
coeff = f.get('coeff')[...]
f.close()

f = h5py.File('var_extract_total.hdf5', 'r')
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

fn.WP(str(theta.size), filename)
fn.WP(str(cmax), filename)

cmat = np.unravel_index(np.arange(cmax), [N_L, N_p, N_q])
cmat = np.array(cmat).T

st = time.time()

vec = np.zeros(theta.size, dtype='complex128')

for ii in xrange(cmax):
# for ii in xrange(10):

    if np.mod(ii, 100) == 0:
        fn.WP(str(ii), filename)

    L, p, q = cmat[ii, :]

    p_vec = np.zeros(p+1)
    p_vec[p] = 1

    tmp = np.zeros(theta.size, dtype='complex128')

    tmp[:], null = gsh.gsh(phi1, phi, phi2, L)
    tmp[:] *= leg.legval(fn.real2comm(et_norm, a, b), p_vec)
    tmp[:] *= np.real(np.exp((1j*2.*np.pi*np.float64(q)*theta)/L_th))
    tmp[:] *= coeff[ii]

    vec[:] += tmp

Ttime = np.round(time.time()-st, 3)
msg = "total interpolation time: %ss" % Ttime
fn.WP(msg, filename)
msg = "interpolation time per point: %s" % (Ttime/theta.size)
fn.WP(msg, filename)

msg = str(vec.shape)
fn.WP(msg, filename)

error = np.abs(np.real(vec) - Y)

msg = "mean error: %s" % np.mean(error)
fn.WP(msg, filename)
msg = "std of error: %s" % np.std(error)
fn.WP(msg, filename)
msg = "min error: %s" % np.min(error)
fn.WP(msg, filename)

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
