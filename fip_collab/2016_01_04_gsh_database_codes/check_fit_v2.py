import numpy as np
import numpy.polynomial.legendre as leg
import gsh_hex_tri_L0_16 as gsh
import db_functions as fn
import h5py
import time


a = 0.0050
b = 0.0085
filename = 'log_test_regression.txt'

f = h5py.File('coeff_total.hdf5', 'r')
coeff = f.get('coeff')[...]
f.close()

f = h5py.File('var_extract_total.hdf5', 'r')
var_set = f.get('var_set')

theta = var_set[:, 0]

X = np.zeros((theta.size, 3), dtype='float64')
X[:, 0] = var_set[:, 1]  # phi1
X[:, 1] = var_set[:, 2]  # phi
X[:, 2] = var_set[:, 3]  # phi2

et_norm = var_set[:, 4]
Y = var_set[:, 5]

f.close()

L_th = np.pi/3.

N_p = 215  # number of GSH bases to evaluate
N_q = 21  # number of cosine bases to evaluate
N_r = 10  # number of legendre bases to evaluate
cmax = N_p*N_q*N_r  # total number of permutations of basis functions

fn.WP(str(theta.size), filename)
fn.WP(str(cmax), filename)

cmat = np.unravel_index(np.arange(cmax), [N_p, N_q, N_r])
cmat = np.array(cmat).T

st = time.time()

f = h5py.File('X_parts.hdf5', 'r')

vec = np.zeros(theta.size, dtype='complex128')

# for ii in xrange(10):
for ii in xrange(cmax):

    if np.mod(ii, 100) == 0:
        fn.WP(str(ii), filename)

    p, q, r = cmat[ii, :]
    basis_p = f.get('p_%s' % p)[...]
    basis_q = f.get('q_%s' % q)[...]
    basis_r = f.get('r_%s' % r)[...]

    ep_set = np.squeeze(basis_p)*basis_q*basis_r

    vec += coeff[ii]*ep_set

f.close()

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
results[:, 1:4] = X
results[:, 4] = et_norm
results[:, 5] = Y
results[:, 6] = vec
results[:, 7] = error
f.create_dataset('results', data=results)
f.close()
